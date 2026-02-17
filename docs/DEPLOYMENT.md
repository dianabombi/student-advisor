# Deployment Guide - Authentication Module

## Pre-Deployment Checklist

### ✅ Code Review
- [ ] All code reviewed and approved
- [ ] Unit tests passing (36/36 tests)
- [ ] Integration tests passing
- [ ] No security vulnerabilities
- [ ] Environment variables documented

### ✅ Database
- [ ] Migration script ready (`001_add_auth_tables.sql`)
- [ ] Database backup created
- [ ] Migration tested on staging
- [ ] Rollback procedure documented

### ✅ Security
- [ ] Strong SECRET_KEY generated
- [ ] Strong JWT_SECRET_KEY generated
- [ ] Token expiration configured
- [ ] HTTPS enabled
- [ ] CORS properly configured

### ✅ Documentation
- [ ] README.md updated
- [ ] AUTH_MODULE.md created
- [ ] API docs generated (/docs, /redoc)
- [ ] Environment variables documented

## Environment Variables Setup

### Production Environment Variables

Create `.env.production` file:

```env
# ============================================
# CRITICAL SECURITY - CHANGE THESE!
# ============================================
SECRET_KEY=<generate-with-openssl-rand-hex-32>
JWT_SECRET_KEY=<generate-with-openssl-rand-hex-32>
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql://codex_user:STRONG_PASSWORD@db:5432/codex_db

# OpenAI API
OPENAI_API_KEY=sk-your-production-api-key

# MinIO Storage
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=production_access_key
MINIO_SECRET_KEY=production_secret_key
MINIO_BUCKET_NAME=codex-prod-documents

# API Configuration
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# Email (if using email verification)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@yourdomain.com
SMTP_PASSWORD=your-smtp-password
SMTP_FROM_EMAIL=noreply@yourdomain.com

# Application
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

### Generate Secure Keys

```bash
# Generate SECRET_KEY
openssl rand -hex 32

# Generate JWT_SECRET_KEY
openssl rand -hex 32

# Generate strong password
openssl rand -base64 24
```

## Database Migration

### 1. Backup Database

```bash
# Create backup
docker compose exec db pg_dump -U postgres codex_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Or with Docker
docker compose exec db pg_dump -U postgres -F c codex_db > backup.dump
```

### 2. Apply Migration

```bash
# Copy migration file to container
docker cp backend/migrations/001_add_auth_tables.sql codex-db:/tmp/

# Execute migration
docker compose exec db psql -U postgres -d codex_db -f /tmp/001_add_auth_tables.sql

# Verify tables created
docker compose exec db psql -U postgres -d codex_db -c "\dt"
```

### 3. Verify Migration

```bash
# Check users table
docker compose exec db psql -U postgres -d codex_db -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='users';"

# Check sessions table
docker compose exec db psql -U postgres -d codex_db -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='sessions';"

# Check cases table
docker compose exec db psql -U postgres -d codex_db -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='cases';"
```

### 4. Rollback (if needed)

```bash
# Run rollback section from migration script
docker compose exec db psql -U postgres -d codex_db -f /tmp/001_add_auth_tables_rollback.sql
```

## Nginx Reverse Proxy Configuration

### nginx.conf

```nginx
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:3000;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (for hot reload)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # Backend API
    location /api {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CRITICAL: Pass cookies and Auth headers
        proxy_pass_request_headers on;
        proxy_set_header Cookie $http_cookie;
        proxy_set_header Authorization $http_authorization;
        
        # CORS Headers (if needed)
        add_header Access-Control-Allow-Origin "https://yourdomain.com" always;
        add_header Access-Control-Allow-Methods "GET, POST, PATCH, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Authorization, Content-Type, Accept" always;
        add_header Access-Control-Allow-Credentials "true" always;
        
        # Handle preflight requests
        if ($request_method = 'OPTIONS') {
            return 204;
        }
    }
    
    # API Documentation
    location /docs {
        proxy_pass http://backend/docs;
        proxy_set_header Host $host;
    }
    
    location /redoc {
        proxy_pass http  /backend/redoc;
        proxy_set_header Host $host;
    }
}
```

### Test Nginx Configuration

```bash
# Test configuration
docker compose exec nginx nginx -t

# Reload Nginx
docker compose exec nginx nginx -s reload
```

## Docker Deployment

### 1. Update docker-compose.yml

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
    restart: unless-stopped
    
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: unless-stopped
    depends_on:
      - db
      
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=codex_db
      - POSTGRES_USER=codex_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
```

### 2. Build and Deploy

```bash
# Build images
docker compose build --no-cache

# Start services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f backend
docker compose logs -f frontend
```

## Testing Deployment

### 1. Health Checks

```bash
# Backend health
curl https://yourdomain.com/api/auth/health

# Expected response:
# {"status":"ok","service":"authentication","token_expiry_minutes":30}
```

### 2. Authentication Flow Test

```bash
# Register user
curl -X POST https://yourdomain.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123"
  }'

# Login
curl -X POST https://yourdomain.com/api/auth/login \
  -d "username=test@example.com&password=password123"

# Expected: JWT token returned
```

### 3. Protected Endpoint Test

```bash
# Get profile (requires token)
curl https://yourdomain.com/api/auth/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Expected: User profile data
```

### 4. Cookie Test (if using cookies)

```bash
# Check cookies are passed through Nginx
curl -v https://yourdomain.com/api/auth/profile \
  -H "Cookie: token=YOUR_JWT_TOKEN"
```

## Production Checklist

### Security
- [ ] HTTPS enabled with valid SSL certificate
- [ ] Strong secrets generated and set
- [ ] CORS configured for production domains only
- [ ] Rate limiting configured (optional but recommended)
- [ ] Security headers added in Nginx
- [ ] Database credentials rotated
- [ ] Admin default password changed

### Monitoring
- [ ] Health check endpoints tested
- [ ] Logging configured (centralized logging recommended)
- [ ] Error tracking setup (Sentry, etc.)
- [ ] Performance monitoring enabled
- [ ] Database backup scheduled

### Testing
- [ ] Registration flow tested
- [ ] Login flow tested
- [ ] Token expiration tested
- [ ] Protected routes tested
- [ ] Role-based access tested
- [ ] Cross-browser testing completed

### Documentation
- [ ] Deployment runbook updated
- [ ] Rollback procedure documented
- [ ] Team trained on new auth system
- [ ] User guide updated

## Rollback Procedure

If deployment fails:

1. **Stop new services**
   ```bash
   docker compose down
   ```

2. **Restore database backup**
   ```bash
   docker compose exec db psql -U postgres -d codex_db < backup.sql
   ```

3. **Revert to previous version**
   ```bash
   git checkout previous-tag
   docker compose up -d
   ```

4. **Verify old system working**
   ```bash
   curl https://yourdomain.com/api/health
   ```

## Post-Deployment

### 1. Monitor for Issues
- Check error logs for 24-48 hours
- Monitor API response times
- Track authentication failure rates
- Watch database performance

### 2. User Communication
- Notify users of new features
- Provide migration guide if needed
- Set up support channels

### 3. Optimization
- Review slow queries
- Adjust token expiration if needed
- Fine-tune rate limits

## Troubleshooting

### Issue: 401 Unauthorized through Nginx
**Cause**: Authorization header not passed  
**Solution**: Verify `proxy_pass_request_headers on;` in nginx.conf

### Issue: Cookies not working
**Cause**: Cookie domain mismatch  
**Solution**: Set cookie domain properly, use HTTPS

### Issue: CORS errors
**Cause**: Origin not allowed  
**Solution**: Add domain to ALLOWED_ORIGINS in .env

### Issue: Token expiring too quickly
**Cause**: ACCESS_TOKEN_EXPIRE_MINUTES too low  
**Solution**: Increase in .env and restart backend

## Support

For issues:
1. Check logs: `docker compose logs backend`
2. Review AUTH_MODULE.md documentation
3. Test endpoints with /docs (Swagger UI)
4. Contact development team

---

**Deployment Date**: ___________  
**Deployed By**: ___________  
**Version**: ___________
