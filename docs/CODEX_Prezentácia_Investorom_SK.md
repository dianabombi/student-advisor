# CODEX - Technický prehľad platformy pre investorov

**Dátum:** 23. decembra 2025  
**Verzia platformy:** 1.0.0  
**Dokument pripravený pre:** Prezentáciu investorom

---

## 📋 Obsah

1. [Všeobecný prehľad](#všeobecný-prehľad)
2. [Bezpečnosť a ochrana dát](#bezpečnosť-a-ochrana-dát)
3. [Jurisdikcie a právny základ](#jurisdikcie-a-právny-základ)
4. [Jazyková podpora](#jazyková-podpora)
5. [AI agenti a automatizácia](#ai-agenti-a-automatizácia)
6. [Technologický stack](#technologický-stack)
7. [Biznis model a monetizácia](#biznis-model-a-monetizácia)
8. [Právna ochrana (UPL)](#právna-ochrana-upl)
9. [Infraštruktúra a škálovateľnosť](#infraštruktúra-a-škálovateľnosť)
10. [Analytika a monitoring](#analytika-a-monitoring)

---

## 🎯 Všeobecný prehľad

**CODEX** - je AI-platforma pre právne konzultácie s technológiou RAG (Retrieval-Augmented Generation), ktorá poskytuje inteligentnú pomoc v právnych otázkach a analýze dokumentov.

### Kľúčové možnosti

- **RAG-chat s právnym AI** - kontextovo závislé odpovede na právne otázky
- **Spracovanie dokumentov** - automatické rozpoznávanie a klasifikácia 14+ typov dokumentov
- **Multijurisdikcionalita** - podpora legislatívy rôznych krajín
- **Viacjazyčnosť** - 10 jazykov rozhrania
- **Systém predplatného** - monetizácia cez trial + platené plány
- **Analytika používateľov** - sledovanie konverzie a ROI marketingu

---

## 🔒 Bezpečnosť a ochrana dát

### 1. Autentifikácia a autorizácia

#### JWT-tokeny (JSON Web Tokens)
- **Algoritmus:** HS256 (HMAC-SHA256)
- **Doba platnosti:** 30 minút
- **Automatické obnovenie:** Áno
- **Ochrana:** Bearer token v HTTP hlavičkách

```python
# Príklad konfigurácie
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

#### Hashovanie hesiel
- **Algoritmus:** PBKDF2-SHA256 s bcrypt
- **Salt:** Automatická generácia pre každé heslo
- **Iterácie:** Zodpovedá štandardom OWASP

```python
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
```

#### Rolový model prístupu (RBAC)
- **Client** - bežný používateľ
- **Lawyer** - právnik s rozšírenými právami
- **Admin** - administrátor systému
- **Partner Lawyer** - partnerský právnik

### 2. Ochrana pred útokmi

#### Rate Limiting (obmedzenie požiadaviek)
- **Globálny limit:** 100 požiadaviek/hodinu
- **Nahrávanie dokumentov:** 20/minútu
- **Prezeranie dokumentov:** 30/minútu
- **Technológia:** SlowAPI

```python
limiter = Limiter(key_func=get_remote_address, default_limits=["100/hour"])
```

#### CORS (Cross-Origin Resource Sharing)
- Nakonfigurované povolené domény
- Ochrana pred CSRF útokmi
- Kontrola metód a hlavičiek

#### Validácia vstupných dát
- **Pydantic** modely pre všetky API endpoints
- Email validácia cez `email-validator`
- Kontrola typov súborov pred spracovaním

### 3. Izolácia dát používateľov

#### Database-level isolation
```python
# Každý používateľ vidí len svoje dokumenty
documents = db.query(Document).filter(Document.user_id == current_user.id).all()
```

#### MinIO Storage isolation
- Samostatné priečinky pre každého používateľa: `uploads/{user_id}/`
- Presigned URLs s obmedzenou dobou platnosti
- Šifrovanie na úrovni objektového úložiska

### 4. Logovanie a audit

#### Structured Logging (structlog)
- **Formát:** JSON pre ľahké parsovanie
- **Úrovne:** INFO, WARNING, ERROR
- **Sledovanie:**
  - Všetky API požiadavky s timingom
  - Registrácie a prihlásenia
  - Nahrávanie dokumentov
  - Chyby a výnimky

```python
logger.info("user_registered",
           user_id=new_user.id,
           email=new_user.email,
           consent_ip=client_ip)
```

### 5. Ochrana tajných kľúčov

#### Environment Variables
- Všetky tajomstvá v [.env](file:///c:/Users/info/OneDrive/Dokumenty/CODEX/.env) súbore (nie v git)
- Povinná validácia pri štarte:

```python
REQUIRED_ENV_VARS = [
    "OPENAI_API_KEY",
    "SECRET_KEY",
    "JWT_SECRET_KEY",
    "DATABASE_URL"
]
```

#### Generovanie bezpečných kľúčov
```bash
openssl rand -hex 32
```

---

## 🌍 Jurisdikcie a právny základ

### Podporované jurisdikcie

| Kód | Krajina | Vlajka | Stav |
|-----|---------|--------|------|
| **SK** | Slovenská Republika | 🇸🇰 | ✅ Aktívna |
| **CZ** | Česká Republika | 🇨🇿 | ✅ Aktívna |
| **PL** | Polska | 🇵🇱 | ✅ Aktívna |
| **UA** | Ukrajina | 🇺🇦 | 🔄 Vo vývoji |
| **DE** | Deutschland | 🇩🇪 | 🔄 Vo vývoji |
| **FR** | France | 🇫🇷 | 🔄 Vo vývoji |
| **ES** | España | 🇪🇸 | 🔄 Vo vývoji |
| **IT** | Italia | 🇮🇹 | 🔄 Vo vývoji |
| **GB** | United Kingdom | 🇬🇧 | 🔄 Vo vývoji |
| **RU** | Россия | 🇷🇺 | 🔄 Vo vývoji |

### Právne dokumenty

#### Dostupné právne základne (Slovensko)
- Občiansky zákonník (Civilný kódex)
- Zmluvy (Zmluvy)
- Náhrada škody (Odškodnenie)

#### Plány rozšírenia
- České zákonodarstvo
- Poľské zákonodarstvo
- Nariadenia EÚ
- Dodatočné odvetvia práva

---

## 🗣️ Jazyková podpora

### 10 plne podporovaných jazykov

| Kód | Jazyk | Stav | Súbor prekladu |
|-----|-------|------|----------------|
| **SK** | Slovenčina | ✅ 100% | `sk/common.json` |
| **CS** | Čeština | ✅ 100% | `cs/common.json` |
| **PL** | Polski | ✅ 100% | `pl/common.json` |
| **EN** | English | ✅ 100% | `en/common.json` |
| **UK** | Українська | ✅ 100% | `uk/common.json` |
| **RU** | Русский | ✅ 100% | `ru/common.json` |
| **DE** | Deutsch | ✅ 100% | `de/common.json` |
| **FR** | Français | ✅ 100% | `fr/common.json` |
| **ES** | Español | ✅ 100% | `es/common.json` |
| **IT** | Italiano | ✅ 100% | `it/common.json` |

### Funkcie lokalizácie

- **Automatické rozpoznanie jazyka** prehliadača
- **Dynamické prepínanie** bez reštartovania
- **Lokalizované AI** - odpovede vo zvolenom jazyku
- **Právne dokumenty** - Terms of Service a Privacy Policy vo všetkých jazykoch

---

## 🤖 AI agenti a automatizácia

### 1. Health Monitor Agent (Agent monitorovania zdravia)

**Súbor:** [backend/agents/health_monitor_lite.py](file:///c:/Users/info/OneDrive/Dokumenty/CODEX/backend/agents/health_monitor_lite.py)

#### Účel
Automatický monitoring stavu všetkých služieb platformy bez cloudových závislostí.

#### Funkcie
- ✅ Kontrola dostupnosti portov (3001, 8001, 5433, 9002, 6379, 5555)
- ✅ HTTP health checks pre webové služby
- ✅ Monitoring systémových zdrojov (CPU, RAM, Disk)
- ✅ Automatické logovanie do JSON formátu
- ✅ Email upozornenia pri problémoch (voliteľne)
- ✅ Web dashboard pre vizualizáciu

#### Monitoring služieb

```python
services = {
    "frontend": {"port": 3001, "url": "http://localhost:3001"},
    "backend": {"port": 8001, "url": "http://localhost:8001/health"},
    "database": {"port": 5433},
    "minio": {"port": 9002},
    "redis": {"port": 6379},
    "flower": {"port": 5555}
}
```

#### Systémové metriky
- **CPU:** Percento využitia (upozornenie pri >80%)
- **Memory:** Využitie RAM v GB a % (upozornenie pri >80%)
- **Disk:** Využitie disku (upozornenie pri >80%)

#### Spustenie
```bash
# Jednorazová kontrola
python health_monitor_lite.py once

# Trvalý monitoring (každých 5 minút)
python health_monitor_lite.py
```

#### Výstupy
- [monitor_logs.json](file:///c:/Users/info/OneDrive/Dokumenty/CODEX/backend/agents/monitor_logs.json) - história kontrol (posledných 100)
- [current_status.json](file:///c:/Users/info/OneDrive/Dokumenty/CODEX/backend/agents/current_status.json) - aktuálny stav
- [dashboard.html](file:///c:/Users/info/OneDrive/Dokumenty/CODEX/backend/agents/dashboard.html) - webové rozhranie

### 2. RAG AI Agent (Agent právnych konzultácií)

**Technológia:** LangChain + OpenAI GPT-4 + pgvector

#### Účel
Inteligentný asistent pre odpovede na právne otázky na základe nahraných dokumentov.

#### Komponenty

**Embeddings Service** (`services/rag/embeddings.py`)
- Generovanie vektorových reprezentácií textov
- Model: OpenAI `text-embedding-ada-002`
- Rozmernosť: 1536 dimenzií

**Retrieval Chain** (`services/rag/retrieval_chain.py`)
- Sémantické vyhľadávanie vo vektorovej databáze
- Top-K dokumentov (predvolene K=5)
- Budovanie kontextu pre GPT-4

**Document Loader** (`services/rag/load_documents.py`)
- Automatický import dokumentov
- Chunking (rozdelenie na fragmenty)
- Ukladanie do PostgreSQL + pgvector

#### Pipeline spracovania požiadavky

```
Otázka používateľa
    ↓
1. Generovanie embedding požiadavky (OpenAI)
    ↓
2. Vector search v pgvector (PostgreSQL)
    ↓
3. Získanie Top-K relevantných dokumentov
    ↓
4. Budovanie kontextového promptu
    ↓
5. Generovanie odpovede (GPT-4)
    ↓
AI odpoveď + zdroje
```

#### Náklady
- **GPT-4:** ~$0.03 za 1K tokenov
- **Embeddings:** ~$0.0001 za 1K tokenov
- **Cachovanie:** Redis pre 10-50x rýchlejšie opakované požiadavky

### 3. Document Processing Agent (Agent spracovania dokumentov)

**Celery Workers** pre asynchrónne spracovanie

#### Účel
Automatické spracovanie nahraných dokumentov: OCR, klasifikácia, extrakcia dát.

#### Funkcie

**OCR Service** (`services/doc_processor/ocr_service.py`)
- Rozpoznávanie textu z PDF a obrázkov
- Poskytovatelia: Mindee (hlavný), Tesseract (záložný)
- Optimalizácia kvality pred OCR

**Classification** (vypnuté v lightweight verzii)
- 14 typov dokumentov: zmluvy, faktúry, sťažnosti atď.
- ML model na báze transformers (vypnuté pre úsporu pamäte)

**Field Extractor** (`services/doc_processor/field_extractor.py`)
- Automatická extrakcia kľúčových polí
- IČO, DIČ, dátumy, sumy, mená, adresy
- Regex + AI-based extraction

**Template Filler** (`services/doc_processor/template_filler.py`)
- Vypĺňanie DOCX šablón
- Placeholder syntax: `{{field_name}}`
- Generovanie hotových dokumentov

#### Podporované typy dokumentov

1. Employment Contract (Pracovná zmluva)
2. Invoice (Faktúra)
3. Lease Agreement (Nájomná zmluva)
4. Service Contract (Zmluva o dielo)
5. Purchase Agreement (Kúpna zmluva)
6. Complaint (Sťažnosť)
7. Power of Attorney (Plná moc)
8. Court Decision (Súdne rozhodnutie)
9. Tax Form (Daňový formulár)
10. Business Registration (Živnostenský list)
11. Receipt (Pokladničný doklad)
12. Bank Statement (Výpis z účtu)
13. Insurance Policy (Poistná zmluva)
14. Other Legal Document (Iný právny dokument)

#### Asynchrónne spracovanie

**Celery Workers** (`celery-worker`)
- Concurrency: 3 paralelné tasky
- Broker: Redis
- Result backend: Redis
- Automatický retry pri chybách

**Celery Beat** (`celery-beat`)
- Plánovanie periodických úloh
- Čistenie starých logov
- Aktualizácia štatistík

**Flower Dashboard** (http://localhost:5555)
- Monitoring Celery úloh
- Štatistiky vykonávania
- Prezeranie chýb

#### WebSocket pre real-time aktualizácie

```python
@app.websocket("/ws/document/{document_id}")
async def websocket_document_progress(websocket, document_id):
    # Odosielanie progresu spracovania v reálnom čase
    # 0-30%: OCR
    # 30-50%: Klasifikácia
    # 50-70%: Extrakcia polí
    # 70-90%: Ukladanie
    # 90-100%: Generovanie summary
```

### 4. Analytics Agent (Agent analytiky)

**Middleware:** `middleware/analytics_middleware.py`

#### Účel
Sledovanie správania používateľov a efektivity marketingu.

#### Metriky

**Visitor Tracking** (Sledovanie návštevníkov)
- Fingerprint (MD5 hash IP + User Agent)
- Prvá a posledná návšteva
- Počet návštev
- UTM parametre (source, medium, campaign)
- Device type, Browser, OS

**Page Views** (Zobrazenia stránok)
- URL a title stránky
- Referrer
- UTM parametre
- Timestamp

**Marketing Campaigns** (Marketingové kampane)
- Názov kampane
- Kanál (Google Ads, Facebook, Instagram, LinkedIn)
- Náklady v EUR
- Dátumy začiatku/konca
- ROI výpočty

#### Dashboard vlastníka

**Súbor:** [backend/analytics_dashboard.html](file:///c:/Users/info/OneDrive/Dokumenty/CODEX/backend/analytics_dashboard.html)

Metriky:
- 📊 Celkový počet návštevníkov
- 👥 Noví vs opakovaní návštevníci
- 📈 Konverzia návštevník → registrácia
- 💰 Náklady na získanie používateľa (CAC)
- 🎯 ROI podľa kanálov
- 📱 Rozdelenie podľa zariadení
- 🌍 Top zdroje návštevnosti

### 5. Support AI Agent (Agent podpory)

**Báza znalostí:** [backend/ai_support_knowledge.txt](file:///c:/Users/info/OneDrive/Dokumenty/CODEX/backend/ai_support_knowledge.txt)

#### Účel
Automatická pomoc používateľom na základe analýzy logov a typických problémov.

#### Funkcie
- Analýza logov pre zistenie chýb
- AI-generovanie riešení na základe bázy znalostí
- Automatické vytváranie tiketov
- Eskalácia k človeku pri potrebe

#### Databáza tiketov

```python
class SupportTicket(Base):
    issue_description = Column(Text)
    ai_response = Column(Text)
    logs_analyzed = Column(Integer)
    errors_found = Column(Integer)
    status = Column(String)  # ai_resolved, needs_human
    needs_human = Column(Boolean)
```

---

## 💻 Technologický stack

### Frontend

| Technológia | Verzia | Účel |
|-------------|--------|------|
| **Next.js** | 14.x | React framework s SSR |
| **TypeScript** | 5.x | Type-safe JavaScript |
| **Tailwind CSS** | 3.x | Utility-first CSS |
| **React Hooks** | 18.x | State management |

### Backend

| Technológia | Verzia | Účel |
|-------------|--------|------|
| **FastAPI** | Latest | Python web framework |
| **Python** | 3.10+ | Programovací jazyk |
| **SQLAlchemy** | 2.x | ORM pre databázy |
| **Alembic** | Latest | Database migrations |
| **Pydantic** | Latest | Data validation |
| **OpenAI API** | Latest | GPT-4, Embeddings |
| **LangChain** | 0.1.0 | RAG framework |

### Databázy

| Technológia | Verzia | Účel |
|-------------|--------|------|
| **PostgreSQL** | Latest | Hlavná DB |
| **pgvector** | Latest | Vector search extension |
| **Redis** | 7-alpine | Cache + message broker |

### Úložisko a spracovanie

| Technológia | Verzia | Účel |
|-------------|--------|------|
| **MinIO** | Latest | S3-kompatibilné objektové úložisko |
| **Celery** | 5.3.4 | Asynchrónne úlohy |
| **Flower** | 2.0.1 | Celery monitoring |

### OCR a spracovanie dokumentov

| Technológia | Verzia | Účel |
|-------------|--------|------|
| **Mindee** | Latest | OCR API (hlavný) |
| **Tesseract** | 0.3.10+ | OCR (záložný) |
| **PyPDF2** | Latest | PDF spracovanie |
| **python-docx** | Latest | DOCX spracovanie |
| **pdfplumber** | 0.10.0+ | PDF text extraction |
| **Pillow** | 10.0.0+ | Image processing |
| **pdf2image** | 1.16.3+ | PDF to image conversion |

### Bezpečnosť

| Technológia | Verzia | Účel |
|-------------|--------|------|
| **python-jose** | Latest | JWT tokens |
| **passlib** | Latest | Password hashing (bcrypt) |
| **slowapi** | 0.1.9 | Rate limiting |

### Monitoring a logovanie

| Technológia | Verzia | Účel |
|-------------|--------|------|
| **structlog** | 24.1.0 | Structured logging |
| **psutil** | Latest | System monitoring |

### Infraštruktúra

| Technológia | Verzia | Účel |
|-------------|--------|------|
| **Docker** | Latest | Kontajnerizácia |
| **Docker Compose** | Latest | Orchestrácia |

---

## 💰 Biznis model a monetizácia

### Systém predplatného

#### 1. Trial Period (Skúšobné obdobie)
- **Trvanie:** 7 dní
- **Cena:** Zadarmo
- **Automatický štart:** Pri registrácii
- **Obmedzenie:** 500 požiadaviek/mesiac
- **Blokovanie:** Automatické po skončení

```python
trial_start = datetime.utcnow()
trial_end = trial_start + timedelta(days=7)
subscription_status = 'trial'
```

#### 2. Platené plány

| Plán | Trvanie | Cena | Úspora |
|------|---------|------|--------|
| **Mesačný** | 1 mesiac | 30 EUR | - |
| **Polročný** | 6 mesiacov | 80 EUR | 47% |
| **Ročný** | 1 rok | 120 EUR | 67% |

#### 3. Obmedzenia používania

```python
class User(Base):
    monthly_request_limit = Column(Integer, default=500)
    requests_used_this_month = Column(Integer, default=0)
```

### Platobná infraštruktúra

#### Database Models

**Subscriptions Table**
```python
class Subscription(Base):
    plan_type = Column(String)  # '1month', '6months', '1year', 'trial'
    amount = Column(Integer)  # V EUR
    status = Column(String)  # pending, active, expired, cancelled
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_trial = Column(Boolean)
```

**Payments Table**
```python
class Payment(Base):
    amount = Column(Integer)  # V EUR
    currency = Column(String, default='EUR')
    status = Column(String)  # pending, completed, failed, refunded
    payment_method = Column(String)  # stripe, paypal, bank_transfer
    transaction_id = Column(String)
    payment_metadata = Column(JSON)
```

#### API Endpoints

```http
POST /api/subscriptions/create
POST /api/payments/initiate
GET /api/subscription/status
POST /api/subscription/cancel
```

#### Integrácie (pripravené na pripojenie)
- Stripe
- PayPal
- Bank transfer
- Ďalšie platobné brány

### Monetizácia nákladov

#### OpenAI API Costs
- Sledovanie v tabuľke [UsageHistory](file:///c:/Users/info/OneDrive/Dokumenty/CODEX/backend/main.py#168-176)
- Výpočet nákladov podľa tokenov
- Logovanie každej požiadavky

```python
class UsageHistory(Base):
    request_type = Column(String)
    tokens_used = Column(Integer)
    cost_estimate = Column(Integer)  # V centoch
```

#### Pricing Strategy
- Trial: Zadarmo (marketing)
- Paid: Pokrytie nákladov + zisk
- Enterprise: Custom pricing

---

## ⚖️ Právna ochrana (UPL)

### Unauthorized Practice of Law Protection

#### Povinné súhlasy pri registrácii

**3 checkboxy (všetky povinné):**

1. **consent_ai_tool** - "Rozumiem, že CODEX je AI nástroj, nie právnik"
2. **consent_no_advice** - "Rozumiem, že CODEX neposkytuje právne poradenstvo"
3. **consent_no_attorney** - "Rozumiem, že používanie CODEX nevytvára vzťah advokát-klient"

#### Sledovanie súhlasu (pre právnu ochranu)

```python
class User(Base):
    # UPL Consent tracking
    consent_ai_tool = Column(Boolean, nullable=False)
    consent_no_advice = Column(Boolean, nullable=False)
    consent_no_attorney = Column(Boolean, nullable=False)
    consent_timestamp = Column(DateTime)
    consent_ip_address = Column(String)
    consent_user_agent = Column(String)
    
    # Version tracking
    consent_terms_version = Column(String, default="1.0")
    consent_upl_version = Column(String, default="1.0")
```

#### Validácia pri registrácii

```python
if not (user_data.consent_ai_tool and 
        user_data.consent_no_advice and 
        user_data.consent_no_attorney):
    raise HTTPException(
        status_code=400,
        detail="All consent acknowledgments are mandatory"
    )
```

#### Logovanie súhlasu

```python
logger.info("user_registered",
           user_id=new_user.id,
           consent_ai_tool=True,
           consent_no_advice=True,
           consent_no_attorney=True,
           consent_ip=client_ip,
           consent_user_agent=user_agent)
```

### Právne dokumenty

#### Terms of Service (Podmienky používania)
- **Súbor:** [frontend/app/terms/page.tsx](file:///c:/Users/info/OneDrive/Dokumenty/CODEX/frontend/app/terms/page.tsx)
- **Jazyky:** 10 jazykov (SK, CS, PL, EN, UK, RU, DE, FR, ES, IT)
- **Verzia:** 1.0
- **Aktualizácia:** Sledované v DB

#### Privacy Policy (Zásady ochrany osobných údajov)
- **Súbor:** [frontend/app/privacy/page.tsx](file:///c:/Users/info/OneDrive/Dokumenty/CODEX/frontend/app/privacy/page.tsx)
- **Jazyky:** 10 jazykov
- **GDPR compliance:** Áno
- **Sekcie:**
  - Zber dát
  - Používanie dát
  - Ochrana dát
  - Práva používateľov
  - Cookies
  - Kontakty DPO

---

## 🏗️ Infraštruktúra a škálovateľnosť

### Docker Architecture

#### Services (7 kontajnerov)

```yaml
services:
  frontend:      # Next.js (port 3001)
  backend:       # FastAPI (port 8001)
  db:            # PostgreSQL + pgvector (port 5433)
  minio:         # Object storage (ports 9002, 9003)
  redis:         # Cache + broker (port 6379)
  celery-worker: # Async tasks
  celery-beat:   # Scheduled tasks
  flower:        # Monitoring (port 5555)
```

#### Volumes (Persistent Storage)

```yaml
volumes:
  postgres_data:  # Database
  minio_data:     # Documents
  redis_data:     # Cache
```

#### Health Checks

Všetky služby majú health checks:
- **Database:** `pg_isready`
- **Redis:** `redis-cli ping`
- **MinIO:** HTTP health endpoint
- **Backend:** `/health` endpoint

### Škálovateľnosť

#### Horizontal Scaling
- **Frontend:** Možno spustiť N replík za load balancer
- **Backend:** Stateless, ľahko škálovateľný
- **Celery Workers:** Pridávanie workers podľa potreby
- **Redis:** Redis Cluster pre veľké zaťaženia

#### Vertical Scaling
- **Database:** Zvýšenie RAM pre cachovanie
- **MinIO:** Pridávanie diskov
- **Celery:** Zvýšenie concurrency

#### Caching Strategy
- **Redis:** Cachovanie výsledkov RAG požiadaviek
- **10-50x rýchlejšie** pre opakované požiadavky
- TTL (Time To Live) nastaviteľné

### Performance

#### Benchmarks
- **Embedding Generation:** 1-2 sekundy/dokument
- **Vector Search:** <500ms
- **Chat Response:** 2-5 sekúnd (závisí od OpenAI)
- **OCR Processing:** 5-30 sekúnd (závisí od veľkosti)

#### Optimization
- **Database Indexes:** Na všetkých foreign keys a search poliach
- **Connection Pooling:** SQLAlchemy pool
- **Async Processing:** Celery pre ťažké úlohy
- **WebSocket:** Real-time updates bez pollingu

---

## 📊 Analytika a monitoring

### 1. Application Monitoring

#### Structured Logging
- **Formát:** JSON
- **Ukladanie:** `backend/logs/`
- **Rotácia:** Automatická
- **Úrovne:** DEBUG, INFO, WARNING, ERROR

#### Metriky v logoch
```json
{
  "event": "api_request",
  "method": "POST",
  "path": "/api/chat",
  "status_code": 200,
  "duration_ms": 2341.56,
  "user_id": 123,
  "timestamp": "2025-12-23T20:00:00Z"
}
```

### 2. Business Analytics

#### Visitor Analytics
- Unikátni návštevníci (fingerprint)
- Zdroje návštevnosti
- UTM tracking
- Device/Browser/OS štatistiky

#### Conversion Funnel
```
Návštevník → Registrácia → Trial → Paid Subscription
```

#### Marketing ROI
```python
ROI = (Revenue - Marketing_Cost) / Marketing_Cost * 100%
```

### 3. System Health

#### Health Monitor Dashboard
- **URL:** `backend/agents/dashboard.html`
- **Aktualizácia:** Každých 5 minút
- **Metriky:**
  - Stav všetkých služieb
  - CPU, RAM, Disk usage
  - História za 24 hodín

#### Flower Dashboard
- **URL:** http://localhost:5555
- **Credentials:** admin/admin (mení sa v .env)
- **Metriky:**
  - Active tasks
  - Task success/failure rate
  - Worker statistics
  - Task history

### 4. Cost Tracking

#### OpenAI Costs
```bash
# Prezeranie nákladov
View_OpenAI_Costs.bat
```

Sledovanie:
- Použité tokeny
- Náklady podľa modelov (GPT-4, embeddings)
- Náklady podľa používateľov
- Trendy nákladov

#### Infrastructure Costs
- Docker resources
- Database storage
- MinIO storage
- Redis memory

---

## 🚀 Deployment a Operations

### Spustenie platformy

#### Automatické spustenie
```bash
START_CODEX_AUTO.bat
```

Vykonáva:
1. ✅ Kontrola Dockeru
2. ✅ Konfigurácia .env
3. ✅ Spustenie všetkých služieb
4. ✅ Otvorenie prehliadača

#### Manuálne spustenie
```bash
Launch CODEX.bat
```

#### Zastavenie
```bash
Stop CODEX.bat
```

### Prístup k platforme

| Služba | URL | Credentials |
|--------|-----|-------------|
| **Main App** | http://localhost:3001 | User account |
| **API Docs** | http://localhost:8001/docs | - |
| **MinIO Console** | http://localhost:9003 | minioadmin/minioadmin |
| **Flower** | http://localhost:5555 | admin/admin |

### Monitoring

```bash
# Kontrola zdravia
Check_Health.bat

# Prezeranie logov
View_Logs.bat

# Prezeranie chýb
View_Errors.bat

# Náklady OpenAI
View_OpenAI_Costs.bat
```

### Backup Strategy

#### Database Backup
```bash
docker exec codex-db-1 pg_dump -U user codex_db > backup.sql
```

#### MinIO Backup
- Automatická replikácia (nastaviteľná)
- Export buckets

#### Configuration Backup
- `.env` súbor (tajné!)
- `docker-compose.yml`

---

## 📈 Konkurenčné výhody

### 1. Technologické
- ✅ **RAG Technology** - najmodernejší prístup k AI
- ✅ **Multi-jurisdiction** - unikátna možnosť
- ✅ **10 Languages** - široký trh
- ✅ **Real-time Processing** - WebSocket updates
- ✅ **Scalable Architecture** - pripravenosť na rast

### 2. Právne
- ✅ **UPL Protection** - plná ochrana pred žalobami
- ✅ **GDPR Compliant** - súlad s EÚ zákonodarstvom
- ✅ **Consent Tracking** - detailný audit súhlasov
- ✅ **Multi-language Legal Docs** - pre všetky trhy

### 3. Biznis
- ✅ **Trial + Subscription** - overený model
- ✅ **Analytics Built-in** - pochopenie používateľov
- ✅ **Marketing ROI Tracking** - optimalizácia nákladov
- ✅ **Automated Support** - zníženie prevádzkových nákladov

### 4. Prevádzkové
- ✅ **Docker-based** - ľahké nasadenie
- ✅ **Health Monitoring** - proaktívne zisťovanie problémov
- ✅ **Structured Logging** - rýchly debugging
- ✅ **Automated Tasks** - minimum manuálnej práce

---

## 🎯 Roadmap a plány rozvoja

### Phase 1: Current (Q4 2025) ✅
- ✅ Core RAG funkcionalita
- ✅ 3 jurisdikcie (SK, CZ, PL)
- ✅ 10 jazykov
- ✅ Trial + Subscription systém
- ✅ Základná analytika

### Phase 2: Q1 2026 🔄
- 🔄 Integrácia platobnej brány (Stripe/PayPal)
- 🔄 Email verifikácia
- 🔄 Reset hesla
- 🔄 Vylepšená klasifikácia dokumentov (ML modely)
- 🔄 Mobilná aplikácia (React Native)

### Phase 3: Q2 2026 📋
- 📋 Dodatočné jurisdikcie (UA, DE, FR)
- 📋 Pokročilý analytický dashboard
- 📋 API pre integrácie tretích strán
- 📋 White-label riešenie pre advokátske kancelárie
- 📋 Enterprise funkcie (SSO, custom branding)

### Phase 4: Q3-Q4 2026 📋
- 📋 AI-generovanie zmlúv
- 📋 Hlasové rozhranie
- 📋 Blockchain pre verifikáciu dokumentov
- 📋 Marketplace pre právne šablóny
- 📋 Partnerský program pre právnikov

---

## 💡 Záver pre investorov

### Prečo je CODEX výhodná investícia?

#### 1. Veľký trh
- **Legal Tech Market:** $28.8B do 2027 (CAGR 13.7%)
- **Target:** SMB, jednotlivci, advokátske kancelárie
- **Geografia:** EÚ + Východná Európa (450M+ obyvateľov)

#### 2. Technologická výhoda
- Používanie najmodernejších AI technológií (GPT-4, RAG)
- Unikátna multijurisdikcionalita
- Škálovateľná architektúra

#### 3. Právna bezpečnosť
- Plná UPL ochrana
- GDPR compliance
- Detailný audit trail

#### 4. Monetizácia
- Overený SaaS model
- Nízke prevádzkové náklady (automatizácia)
- Vysoký lifetime value (LTV)

#### 5. Tím a vykonávanie
- Fungujúci produkt (nie prototyp)
- Kompletná dokumentácia
- Pripravenosť na škálovanie

### Finančné ukazovatele (prognóza)

#### Year 1
- **Users:** 1,000 (trial) → 100 paid (10% konverzia)
- **MRR:** €3,000 (100 users × €30/mesiac)
- **ARR:** €36,000

#### Year 2
- **Users:** 10,000 (trial) → 1,500 paid (15% konverzia)
- **MRR:** €45,000
- **ARR:** €540,000

#### Year 3
- **Users:** 50,000 (trial) → 10,000 paid (20% konverzia)
- **MRR:** €300,000
- **ARR:** €3,600,000

### Požadovaná investícia

**Suma:** €500,000 - €1,000,000

**Použitie:**
- 40% - Marketing (Google Ads, Facebook, LinkedIn)
- 30% - Rozšírenie tímu (vývojári, právni experti)
- 20% - Infraštruktúra (škálovanie, bezpečnosť)
- 10% - Právna compliance (dodatočné jurisdikcie)

**Equity:** 15-25% (dohodnuteľné)

---

## 📞 Kontakty

**Platforma:** CODEX Legal AI  
**Verzia:** 1.0.0  
**Dátum:** 23. decembra 2025

**Pre investorské otázky:**
- Email: investors@codex-legal.ai
- Webstránka: https://codex-legal.ai
- Demo: http://localhost:3001

---

**Dokument pripravený:** 23. decembra 2025  
**Dôvernosť:** Len pre investorov  
**© 2025 CODEX Legal AI. Všetky práva vyhradené.**
