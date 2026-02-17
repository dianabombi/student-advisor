# Student - AI Educational Platform

**Student** is an advanced AI-powered educational consultation platform featuring intelligent course recommendations, document analysis, and personalized learning assistance.

## 🎯 Key Features

### 🤖 AI-Powered Learning Assistant
- **Intelligent Q&A**: Ask educational questions and get context-aware answers
- **Course Recommendations**: AI suggests courses based on your goals and background
- **Study Planning**: Personalized study schedules and learning paths
- **Multi-turn Conversations**: Maintains conversation context

### 📚 Document Management
- **Smart Upload**: Automatic text extraction from PDF, DOCX, images
- **Transcript Analysis**: Analyze academic transcripts and certificates
- **Diploma Recognition**: Check diploma recognition requirements
- **Application Documents**: Organize university application materials

### 🌍 Multi-Language Support
- **10 Languages**: Slovak, Czech, Polish, English, German, French, Spanish, Italian, Ukrainian, Russian
- **Localized UI**: Full interface translation
- **Language-Aware AI**: Responds in your preferred language

### 🔒 Authentication & Authorization
- **User Registration & Login**: Secure JWT-based authentication
- **Role-Based Access Control**: Student, Consultant, Admin roles
- **Protected Routes**: Middleware-based route protection
- **Session Management**: Automatic token refresh and expiration

### 🎓 Educational Features
- **University Search**: Find and compare universities across Europe
- **Course Catalog**: Browse thousands of courses and programs
- **Application Tracking**: Track your university applications
- **Consultant Marketplace**: Connect with educational consultants
- **Document Verification**: Verify and validate educational documents

## 🚀 Quick Start

### Prerequisites

- **Docker Desktop** (required)
- **OpenAI API Key** (required for AI features)
  - Get yours at: https://platform.openai.com/api-keys

### 1. Configure Environment Variables

Copy the example file and edit:
```bash
cp .env.example .env
```

**Required changes:**
- `OPENAI_API_KEY`: Your OpenAI API key
- `SECRET_KEY`: Generate with `openssl rand -hex 32`
- `JWT_SECRET_KEY`: Generate with `openssl rand -hex 32`

### 2. Launch Platform

**Automatic Launch:**
```bash
START_STUDENT_AUTO.bat
```

**Manual Launch:**
```bash
Launch Student.bat
```

### 3. Access the Platform

- **Main App**: http://localhost:3002
- **API Docs**: http://localhost:8002/docs
- **MinIO Console**: http://localhost:9005
  - Username: `minioadmin`
  - Password: `minioadmin`
- **Flower Monitoring**: http://localhost:5556

### 4. First Steps

1. **Register** a new account
2. **Upload** your academic documents
3. **Search** for universities and courses
4. **Chat** with AI educational assistant
5. **Connect** with educational consultants

## 🏗️ Architecture

### Technology Stack

**Frontend**
- Next.js 14 with TypeScript
- Tailwind CSS for styling
- Modern educational design inspired by Coursera

**Backend**
- FastAPI (Python)
- OpenAI API (GPT-4, Embeddings)
- PostgreSQL with pgvector
- Redis for caching

**Infrastructure**
- Docker Compose orchestration
- MinIO for document storage
- JWT authentication

### Services

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 3001 | Next.js web app |
| Backend | 8001 | FastAPI server |
| Database | 5433 | PostgreSQL + pgvector |
| MinIO | 9002, 9003 | Object storage |
| Redis | 6379 | Cache & message broker |

## 📊 Monitoring

Access monitoring dashboard at http://localhost:5555

## 🛠️ Development

### Rebuild Services

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

### View Logs

```bash
docker compose logs -f
```

### Stop Platform

```bash
docker compose down
```

## 📝 License

Proprietary - All rights reserved

## 🤝 Support

For issues or questions, contact the development team.

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-09  
**Educational Platform for European Students**
