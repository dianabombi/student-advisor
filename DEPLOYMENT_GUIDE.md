# Deployment Guide: Document Processing Module

## Overview

This guide covers deploying the Document Processing module to staging and production environments.

## Pre-Deployment Checklist

### Code Quality

- [x] All unit tests passing (20 tests)
- [x] All integration tests passing (20+ tests)
- [x] Code review completed
- [x] No linting errors
- [x] Documentation updated

### Database

- [ ] Database migrations prepared
- [ ] Backup created
- [ ] Migration tested on staging
- [ ] Rollback plan ready

### Dependencies

- [x] All new dependencies documented in `requirements.txt`
- [ ] Dependencies security audit completed
- [ ] No known vulnerabilities

### Configuration

- [ ] Environment variables configured
- [ ] MinIO buckets created
- [ ] OCR service configured
- [ ] API keys secured

### Testing

- [x] Unit tests: 85%+ coverage ✅
- [x] Integration tests: Full pipeline ✅
- [ ] Load testing completed
- [ ] Security testing completed

---

## Deployment Steps

### 1. Pre-Deployment Preparation

#### Backup Current System

```bash
# Backup database
docker exec codex-db pg_dump -U postgres codex_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup MinIO data
docker exec codex-minio mc mirror /data /backup

# Tag current version
git tag -a v1.0.0-pre-document-processing -m "Before document processing deployment"
```

#### Run Final Tests

```bash
# Backend tests
cd backend
pytest tests/ -v --cov

# Integration tests
pytest tests/test_api_integration.py -v
```

### 2. Database Migration

#### Create Migration

```sql
-- Add DocumentProcessingJob table
CREATE TABLE IF NOT EXISTS document_processing_jobs (
    id SERIAL PRIMARY KEY,
    document_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    filename VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    document_type VARCHAR(100),
    confidence FLOAT,
    extracted_fields JSONB,
    summary TEXT,
    error_message TEXT,
    raw_object_name VARCHAR(500),
    processed_object_name VARCHAR(500),
    filled_template_path VARCHAR(500),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_started_at TIMESTAMP,
    processed_at TIMESTAMP,
    metadata JSONB
);

CREATE INDEX idx_document_processing_jobs_user_id ON document_processing_jobs(user_id);
CREATE INDEX idx_document_processing_jobs_status ON document_processing_jobs(status);
CREATE INDEX idx_document_processing_jobs_uploaded_at ON document_processing_jobs(uploaded_at DESC);
```

#### Apply Migration

```bash
# Staging
docker exec -it codex-db-staging psql -U postgres -d codex_db -f migration.sql

# Production (after staging validation)
docker exec -it codex-db-prod psql -U postgres -d codex_db -f migration.sql
```

### 3. MinIO Setup

#### Create Buckets

```bash
# Connect to MinIO
docker exec -it codex-minio mc alias set myminio http://localhost:9002 minioadmin minioadmin

# Create buckets
docker exec -it codex-minio mc mb myminio/raw-docs
docker exec -it codex-minio mc mb myminio/processed-docs
docker exec -it codex-minio mc mb myminio/templates
docker exec -it codex-minio mc mb myminio/filled-docs

# Set policies
docker exec -it codex-minio mc anonymous set download myminio/raw-docs
docker exec -it codex-minio mc anonymous set download myminio/processed-docs
docker exec -it codex-minio mc anonymous set download myminio/filled-docs
```

### 4. Backend Deployment

#### Update Dependencies

```bash
cd backend

# Install new dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(pytest|httpx|python-docx|pytesseract)"
```

#### Deploy to Staging

```bash
# Build new image
docker-compose -f docker-compose.staging.yml build backend

# Deploy
docker-compose -f docker-compose.staging.yml up -d backend

# Check logs
docker-compose -f docker-compose.staging.yml logs -f backend
```

#### Verify Staging

```bash
# Health check
curl http://staging.codex.example.com/health

# Test document upload
curl -X POST "http://staging.codex.example.com/api/documents/upload" \
  -H "Authorization: Bearer {token}" \
  -F "file=@test_contract.pdf"
```

### 5. Frontend Deployment

#### Build Frontend

```bash
cd frontend

# Install dependencies
npm install

# Build production
npm run build

# Test build
npm run start
```

#### Deploy to Staging

```bash
# Build Docker image
docker-compose -f docker-compose.staging.yml build frontend

# Deploy
docker-compose -f docker-compose.staging.yml up -d frontend

# Verify
curl http://staging.codex.example.com
```

### 6. Production Deployment

**⚠️ Production Checklist:**

- [ ] Staging fully tested (24+ hours)
- [ ] No critical bugs reported
- [ ] Performance metrics acceptable
- [ ] Security scan completed
- [ ] Backup verified
- [ ] Rollback plan ready
- [ ] Monitoring configured
- [ ] Team notified

#### Deploy to Production

```bash
# Stop services momentarily (optional - for zero-downtime use rolling update)
docker-compose -f docker-compose.prod.yml stop backend frontend

# Pull latest images
docker-compose -f docker-compose.prod.yml pull

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Verify
curl https://codex.example.com/health
```

### 7. Post-Deployment Verification

#### Smoke Tests

```bash
# Run automated smoke tests
./scripts/smoke-tests.sh production

# Manual verification checklist:
# [ ] Homepage loads
# [ ] Login works
# [ ] Document upload works
# [ ] Processing completes
# [ ] Results display correctly
# [ ] Admin template management works
```

#### Monitor Logs

```bash
# Backend logs
docker-compose logs -f backend | grep -i error

# Check processing jobs
docker exec -it codex-db psql -U postgres -d codex_db \
  -c "SELECT status, COUNT(*) FROM document_processing_jobs GROUP BY status;"
```

---

## Rollback Procedure

### If Issues Occur

**Immediate Actions:**

1. **Stop traffic to new version**
```bash
# Revert to previous version
docker-compose -f docker-compose.prod.yml down
git checkout v1.0.0-pre-document-processing
docker-compose -f docker-compose.prod.yml up -d
```

2. **Restore database if needed**
```bash
docker exec -i codex-db psql -U postgres codex_db < backup_YYYYMMDD_HHMMSS.sql
```

3. **Notify team**
```bash
# Send alert
./scripts/send-alert.sh "Production rollback initiated"
```

### Rollback Steps

```bash
# 1. Stop current services
docker-compose -f docker-compose.prod.yml down

# 2. Checkout previous version
git checkout v1.0.0-pre-document-processing

# 3. Rebuild if needed
docker-compose -f docker-compose.prod.yml build

# 4. Restore database
docker exec -i codex-db psql -U postgres codex_db < backup.sql

# 5. Start services
docker-compose -f docker-compose.prod.yml up -d

# 6. Verify
curl https://codex.example.com/health
```

---

## Monitoring

### Key Metrics

**System Health:**
- API response times (< 500ms)
- Document processing time (< 30s average)
- Error rate (< 1%)
- Database connections
- MinIO storage usage

**Business Metrics:**
- Documents processed per day
- Success rate by document type
- Average confidence scores
- Template usage statistics

### Monitoring Setup

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'codex-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'

  - job_name: 'minio'
    static_configs:
      - targets: ['minio:9000']
```

### Alerts

```yaml
# alerting_rules.yml
groups:
  - name: codex_alerts
    rules:
      - alert: HighProcessingFailureRate
        expr: rate(processing_failures[5m]) > 0.1
        for: 5m
        annotations:
          summary: "High document processing failure rate"
      
      - alert: SlowProcessing
        expr: histogram_quantile(0.95, processing_duration_seconds) > 60
        for: 10m
        annotations:
          summary: "Document processing is slow"
```

---

## Environment-Specific Configuration

### Staging

```env
# .env.staging
ENVIRONMENT=staging
DEBUG=false
DATABASE_URL=postgresql://user:pass@db-staging:5432/codex_staging
MINIO_ENDPOINT=minio-staging:9000
OPENAI_API_KEY=sk-staging-key
LOG_LEVEL=DEBUG
```

### Production

```env
# .env.production
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://user:pass@db-prod:5432/codex_prod
MINIO_ENDPOINT=minio-prod:9000
OPENAI_API_KEY=sk-prod-key
LOG_LEVEL=INFO
SENTRY_DSN=https://...
```

---

## Troubleshooting

### Common Issues

**1. OCR Service Not Working**
```bash
# Check Tesseract installation
docker exec -it codex-backend tesseract --version

# Install if missing
docker exec -it codex-backend apt-get update && apt-get install -y tesseract-ocr
```

**2. MinIO Connection Failed**
```bash
# Check MinIO status
docker exec -it codex-minio mc admin info myminio

# Recreate buckets if needed
docker exec -it codex-minio mc mb myminio/raw-docs
```

**3. Database Migration Failed**
```bash
# Check current schema
docker exec -it codex-db psql -U postgres -d codex_db -c "\dt"

# Manual rollback
docker exec -it codex-db psql -U postgres -d codex_db -c "DROP TABLE document_processing_jobs;"
```

**4. High Memory Usage**
```bash
# Check container stats
docker stats codex-backend

# Restart if needed
docker-compose restart backend
```

---

## Maintenance

### Regular Tasks

**Daily:**
- [ ] Check error logs
- [ ] Monitor processing times
- [ ] Review failed jobs

**Weekly:**
- [ ] Review storage usage
- [ ] Clean up old processed documents
- [ ] Update dependencies (security patches)

**Monthly:**
- [ ] Full system backup
- [ ] Performance review
- [ ] Security audit

### Cleanup Scripts

```bash
# Clean old processed documents (90+ days)
docker exec -it codex-db psql -U postgres -d codex_db -c \
  "DELETE FROM document_processing_jobs WHERE processed_at < NOW() - INTERVAL '90 days';"

# Clean MinIO old files
docker exec -it codex-minio mc rm --recursive --force \
  --older-than 90d myminio/processed-docs/
```

---

## Support Contacts

**On-Call Engineer:** +1 XXX-XXX-XXXX  
**DevOps Team:** devops@codex.example.com  
**Escalation:** cto@codex.example.com

**Documentation:**
- API Docs: https://docs.codex.example.com
- Runbook: https://wiki.codex.example.com/runbook
- Incident Response: https://wiki.codex.example.com/incidents

---

**Version:** 1.0.0  
**Last Updated:** 2024-12-04  
**Next Review:** 2025-01-04
