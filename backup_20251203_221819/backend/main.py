import os
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
import openai
from services.ocr_service import OCRService, OCRProvider, classify_document
from config.practice_areas import (
    PRACTICE_AREAS, 
    LEGAL_DOCUMENT_TYPES, 
    JURISDICTIONS,
    get_enabled_jurisdictions
)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/codex_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# OCR Service setup
OCR_PROVIDER = os.getenv("OCR_PROVIDER", "mindee")  # mindee, tesseract, veryfi, klippa
ocr_service = OCRService(provider=OCRProvider(OCR_PROVIDER))

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    documents = relationship("Document", back_populates="owner")
    messages = relationship("ChatMessage", back_populates="user")

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    document_type = Column(String)  # contract, lawsuit, complaint, etc.
    jurisdiction = Column(String, default="SK")  # SK, CZ, PL, etc.
    practice_area = Column(String)  # civil, criminal, commercial, etc.
    legal_category = Column(String)  # More specific categorization
    extracted_data = Column(JSON)  # OCR extracted data
    confidence = Column(Integer)  # OCR confidence score
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="documents")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="messages")

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class DocumentResponse(BaseModel):
    id: int
    filename: str
    document_type: Optional[str]
    extracted_data: Optional[dict]
    confidence: Optional[int]
    uploaded_at: datetime

# FastAPI app
app = FastAPI(title="CODEX Legal API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auth helpers
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to CODEX Legal API", "version": "0.1.0", "service": "Legal Consultation Platform"}

@app.get("/health")
def health_check():
    return {"status": "ok", "database": "connected", "ocr_provider": OCR_PROVIDER}

# Configuration endpoints
@app.get("/api/practice-areas")
def get_practice_areas():
    """Get all available legal practice areas"""
    return {"practice_areas": PRACTICE_AREAS}

@app.get("/api/jurisdictions")
def get_jurisdictions():
    """Get all supported jurisdictions"""
    return {"jurisdictions": get_enabled_jurisdictions()}

@app.get("/api/document-types")
def get_document_types():
    """Get all legal document types"""
    return {"document_types": LEGAL_DOCUMENT_TYPES}

# Auth endpoints
@app.post("/api/auth/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": new_user.email})
    user_response = UserResponse(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        created_at=new_user.created_at
    )
    
    return {"access_token": access_token, "token_type": "bearer", "user": user_response}

@app.post("/api/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    user_response = UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at
    )
    
    return {"access_token": access_token, "token_type": "bearer", "user": user_response}

# Documents endpoints
@app.get("/api/documents", response_model=List[DocumentResponse])
def get_documents(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    return documents

@app.post("/api/documents/upload")
async def upload_document(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    uploaded_files = []
    
    for file in files:
        # Save file temporarily
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Classify document type
        doc_type = await classify_document(file_path)
        
        # Process with OCR
        try:
            extracted_data = await ocr_service.process_document(file_path, doc_type)
            confidence = int(extracted_data.get('confidence', 0) * 100)
        except Exception as e:
            print(f"OCR processing failed: {e}")
            extracted_data = {}
            confidence = 0
        
        # Save to database
        new_doc = Document(
            filename=file.filename,
            file_path=file_path,
            document_type=doc_type,
            extracted_data=extracted_data,
            confidence=confidence,
            user_id=current_user.id
        )
        db.add(new_doc)
        
        uploaded_files.append({
            "filename": file.filename,
            "type": doc_type,
            "confidence": confidence,
            "data": extracted_data
        })
    
    db.commit()
    return {"message": "Files uploaded and processed", "files": uploaded_files}

@app.get("/api/documents/{document_id}")
def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document

# Chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Save user message
    user_message = ChatMessage(
        user_id=current_user.id,
        role="user",
        content=request.message
    )
    db.add(user_message)
    
    # Get user's documents for context
    recent_docs = db.query(Document).filter(
        Document.user_id == current_user.id
    ).order_by(Document.uploaded_at.desc()).limit(5).all()
    
    # Build context from documents
    context = "Právne dokumenty používateľa:\n"
    for doc in recent_docs:
        doc_info = f"- {doc.filename}"
        if doc.document_type:
            doc_info += f" (Typ: {doc.document_type})"
        if doc.practice_area:
            doc_info += f" (Oblasť: {doc.practice_area})"
        if doc.jurisdiction:
            doc_info += f" (Jurisdikcia: {doc.jurisdiction})"
        context += doc_info + "\n"
    
    # Get AI response
    try:
        system_prompt = """Ste odborný právny konzultant špecializujúci sa na slovenské právo, predovšetkým civilné právo.

Vaše úlohy:
- Poskytovať presné a profesionálne právne poradenstvo založené na slovenských zákonoch a právnych predpisoch
- Odpovedať na otázky týkajúce sa Občianskeho zákonníka SR, Obchodného zákonníka SR a ďalších relevantných právnych predpisov
- Pomáhať s výkladom právnych dokumentov a zmlúv
- Poskytovať všeobecné právne informácie (nie konkrétne právne zastupovanie)

Dôležité upozornenie: Vaše odpovede sú všeobecného informatívneho charakteru a nepredstavujú právne zastupovanie. Pre konkrétne právne prípady odporúčajte konzultáciu s advokátom.

Odpovedajte v slovenčine, jasne, zrozumiteľne a profesionálne."""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"{system_prompt}\n\n{context}"},
                {"role": "user", "content": request.message}
            ]
        )
        ai_response = response.choices[0].message.content
    except Exception as e:
        ai_response = "Prepáčte, momentálne nemôžem spracovať vašu otázku. Skúste to prosím neskôr."
    
    # Save AI response
    assistant_message = ChatMessage(
        user_id=current_user.id,
        role="assistant",
        content=ai_response
    )
    db.add(assistant_message)
    db.commit()
    
    return {"response": ai_response}
