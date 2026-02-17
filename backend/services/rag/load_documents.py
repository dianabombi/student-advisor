    """
    Loads documents from various sources and generates embeddings.
    
    Supports:
    - Local filesystem (PDF, DOCX, TXT)
    - MinIO object storage
    - Automatic text extraction
    - Chunking and embedding generation
    """
    
    def __init__(
        self,
        db_url: str,
        openai_api_key: str,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):
        """
        Initialize document loader.
        
        Args:
            db_url: PostgreSQL connection URL
            openai_api_key: OpenAI API key for embeddings
            chunk_size: Maximum tokens per chunk
            chunk_overlap: Token overlap between chunks
        """
        # Database setup
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # OpenAI embeddings
        os.environ['OPENAI_API_KEY'] = openai_api_key
        self.embeddings_model = OpenAIEmbeddings()
        
        # Text splitter for chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        # MinIO client (lazy initialization)
        self._minio_client = None
    
    def _get_minio_client(self) -> Minio:
        """Get or create MinIO client."""
        if self._minio_client is None:
            self._minio_client = Minio(
                "localhost:9002",
                access_key=os.getenv("MINIO_ROOT_USER", "minioadmin"),
                secret_key=os.getenv("MINIO_ROOT_PASSWORD", "minioadmin"),
                secure=False
            )
        return self._minio_client
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error extracting PDF {file_path}: {e}")
        return text
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        text = ""
        try:
            doc = DocxDocument(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error extracting DOCX {file_path}: {e}")
        return text
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading TXT {file_path}: {e}")
            return ""
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from document based on file extension.
        
        Args:
            file_path: Path to document file
            
        Returns:
            Extracted text content
        """
        ext = Path(file_path).suffix.lower()
        
        if ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            return self.extract_text_from_docx(file_path)
        elif ext == '.txt':
            return self.extract_text_from_txt(file_path)
        else:
            print(f"Unsupported file type: {ext}")
            return ""
    
    def load_from_local(self, directory: str) -> List[Dict]:
        """
        Load documents from local filesystem.
        
        Args:
            directory: Path to directory containing documents
            
        Returns:
            List of document dictionaries
        """
        documents = []
        path = Path(directory)
        
        if not path.exists():
            print(f"Directory not found: {directory}")
            return documents
        
        # Supported extensions
        extensions = ['.pdf', '.docx', '.doc', '.txt']
        
        for file_path in path.rglob('*'):
            if file_path.suffix.lower() in extensions:
                print(f"Loading: {file_path.name}")
                
                text = self.extract_text(str(file_path))
                if text.strip():
                    documents.append({
                        'filename': file_path.name,
                        'content': text,
                        'source': 'local',
                        'path': str(file_path)
                    })
        
        print(f"Loaded {len(documents)} documents from local filesystem")
        return documents
    
    def load_from_minio(self, bucket_name: str, prefix: str = "") -> List[Dict]:
        """
        Load documents from MinIO bucket.
        
        Args:
            bucket_name: MinIO bucket name
            prefix: Optional prefix to filter objects
            
        Returns:
            List of document dictionaries
        """
        documents = []
        client = self._get_minio_client()
        
        try:
            # Check if bucket exists
            if not client.bucket_exists(bucket_name):
                print(f"Bucket '{bucket_name}' does not exist")
                return documents
            
            # List objects
            objects = client.list_objects(bucket_name, prefix=prefix, recursive=True)
            
            for obj in objects:
                # Download to temp file
                temp_path = f"/tmp/{obj.object_name}"
                os.makedirs(os.path.dirname(temp_path), exist_ok=True)
                
                print(f"Downloading: {obj.object_name}")
                client.fget_object(bucket_name, obj.object_name, temp_path)
                
                # Extract text
                text = self.extract_text(temp_path)
                if text.strip():
                    documents.append({
                        'filename': os.path.basename(obj.object_name),
                        'content': text,
                        'source': 'minio',
                        'path': f"{bucket_name}/{obj.object_name}"
                    })
                
                # Cleanup temp file
                os.remove(temp_path)
        
        except S3Error as e:
            print(f"MinIO error: {e}")
        
        print(f"Loaded {len(documents)} documents from MinIO")
        return documents
    
    async def process_document(
        self,
        filename: str,
        content: str,
        metadata: Optional[Dict] = None,
        db: Session = None
    ) -> int:
        """
        Process document: chunk, embed, and store in database.
        
        Args:
            filename: Document filename
            content: Document text content
            metadata: Optional metadata (document_type, practice_area, etc.)
            db: Database session
            
        Returns:
            Number of chunks created
        """
        close_db = False
        if db is None:
            db = self.SessionLocal()
            close_db = True
        
        try:
            # Create document record
            insert_doc = text("""
                INSERT INTO documents (filename, file_path, document_type, practice_area, jurisdiction, extracted_data, confidence, uploaded_at, user_id)
                VALUES (:filename, :file_path, :doc_type, :practice_area, :jurisdiction, :extracted_data, :confidence, :uploaded_at, :user_id)
                RETURNING id
            """)
            
            metadata = metadata or {}
            result = db.execute(insert_doc, {
                'filename': filename,
                'file_path': metadata.get('path', filename),
                'doc_type': metadata.get('document_type', 'legal_reference'),
                'practice_area': metadata.get('practice_area'),
                'jurisdiction': metadata.get('jurisdiction', 'SK'),
                'extracted_data': {'text': content, 'source': metadata.get('source', 'import')},
                'confidence': 100,
                'uploaded_at': datetime.utcnow(),
                'user_id': metadata.get('user_id', 1)  # System user
            })
            
            document_id = result.fetchone()[0]
            print(f"Created document record: ID={document_id}")
            
            # Chunk the text
            chunks = self.text_splitter.split_text(content)
            print(f"Split into {len(chunks)} chunks")
            
            # Generate embeddings (batch processing)
            print("Generating embeddings...")
            embeddings = self.embeddings_model.embed_documents(chunks)
            
            # Insert chunks with embeddings
            insert_chunk = text("""
                INSERT INTO document_chunks (document_id, chunk_index, content, embedding, chunk_metadata, created_at)
                VALUES (:doc_id, :idx, :content, :embedding, :metadata, :created_at)
            """)
            
            for idx, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
                db.execute(insert_chunk, {
                    'doc_id': document_id,
                    'idx': idx,
                    'content': chunk_text,
                    'embedding': embedding,
                    'metadata': {
                        'document_type': metadata.get('document_type'),
                        'practice_area': metadata.get('practice_area'),
                        'jurisdiction': metadata.get('jurisdiction', 'SK'),
                        'filename': filename
                    },
                    'created_at': datetime.utcnow()
                })
            
            db.commit()
            print(f"✅ Stored {len(chunks)} chunks for '{filename}'")
            return len(chunks)
        
        except Exception as e:
            db.rollback()
            print(f"❌ Error processing '{filename}': {e}")
            return 0
        
        finally:
            if close_db:
                db.close()
    
    async def load_and_process(
        self,
        source: str,
        path: str = None,
        bucket: str = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Load documents from source and process them.
        
        Args:
            source: 'local' or 'minio'
            path: Local directory path (for local source)
            bucket: MinIO bucket name (for minio source)
            metadata: Optional metadata to apply to all documents
            
        Returns:
            Summary statistics
        """
        # Load documents
        if source == 'local':
            if not path:
                raise ValueError("Path required for local source")
            documents = self.load_from_local(path)
        elif source == 'minio':
            if not bucket:
                raise ValueError("Bucket required for minio source")
            documents = self.load_from_minio(bucket)
        else:
            raise ValueError(f"Unknown source: {source}")
        
        # Process documents
        total_chunks = 0
        successful = 0
        
        for doc in documents:
            doc_metadata = {**metadata, **doc} if metadata else doc
            chunks = await self.process_document(
                filename=doc['filename'],
                content=doc['content'],
                metadata=doc_metadata
            )
            
            if chunks > 0:
                successful += 1
                total_chunks += chunks
        
        return {
            'total_documents': len(documents),
            'successful': successful,
            'failed': len(documents) - successful,
            'total_chunks': total_chunks
        }


async def main():
    """Main entry point for document loading script."""
    parser = argparse.ArgumentParser(description='Load legal documents into CODEX RAG system')
    parser.add_argument('--source', choices=['local', 'minio'], required=True,
                       help='Document source')
    parser.add_argument('--path', help='Local directory path')
    parser.add_argument('--bucket', help='MinIO bucket name')
    parser.add_argument('--practice-area', help='Practice area code')
    parser.add_argument('--jurisdiction', default='SK', help='Jurisdiction code')
    parser.add_argument('--document-type', default='legal_reference', help='Document type')
    
    args = parser.parse_args()
    
    # Get configuration from environment
    db_url = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5433/codex_db')
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key == 'your_key_here':
        print("❌ Error: OPENAI_API_KEY not configured")
        print("Please set your OpenAI API key in the .env file")
        return
    
    # Create loader
    loader = DocumentLoader(db_url=db_url, openai_api_key=api_key)
    
    # Prepare metadata
    metadata = {
        'practice_area': args.practice_area,
        'jurisdiction': args.jurisdiction,
        'document_type': args.document_type
    }
    
    # Load and process
    print(f"\n🚀 Starting document import from {args.source}...")
    print(f"Configuration: {metadata}\n")
    
    stats = await loader.load_and_process(
        source=args.source,
        path=args.path,
        bucket=args.bucket,
        metadata=metadata
    )
    
    # Print summary
    print("\n" + "="*50)
    print("📊 Import Summary")
    print("="*50)
    print(f"Total documents: {stats['total_documents']}")
    print(f"Successful: {stats['successful']}")
    print(f"Failed: {stats['failed']}")
    print(f"Total chunks created: {stats['total_chunks']}")
    print("="*50)


if __name__ == '__main__':
    asyncio.run(main())
