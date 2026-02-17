# Admin Panel Production Deployment Checklist

**Security & Deployment Guide for Production Environment**

Version 1.0 | Last Updated: February 2026

---

## Overview

This checklist ensures your admin panel is secure and production-ready. Complete ALL items before deploying to production.

> ⚠️ **Critical:** Skipping security steps can lead to data breaches and unauthorized access!

---

## Pre-Deployment Checklist

### ☐ 1. Change Default Admin Password

**Priority:** 🔴 CRITICAL

**Why:** Default credentials are publicly known and a major security risk.

**Steps:**

#### Option A: Via Settings Page (Recommended)
1. Login with default credentials
2. Navigate to Settings (or Profile)
3. Change password to strong password
4. Logout and login with new password

#### Option B: Via Database Script
```python
# backend/scripts/change_admin_password.py
import os
from sqlalchemy import create_engine, text
import bcrypt

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

NEW_PASSWORD = "YourSecurePassword123!@#"  # Change this!
ADMIN_EMAIL = "admin@student.com"

hashed = bcrypt.hashpw(NEW_PASSWORD.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')

with engine.connect() as conn:
    conn.execute(
        text("UPDATE users SET hashed_password = :pwd WHERE email = :email"),
        {'pwd': hashed, 'email': ADMIN_EMAIL}
    )
    conn.commit()
    print(f"✅ Password changed for {ADMIN_EMAIL}")
```

**Run:**
```bash
python backend/scripts/change_admin_password.py
```

**Password Requirements:**
- ✅ Minimum 12 characters
- ✅ Mix of uppercase and lowercase
- ✅ Include numbers
- ✅ Include special characters (!@#$%^&*)
- ✅ Not a dictionary word
- ✅ Unique (not used elsewhere)

**Example Strong Password:** `Adm!n2026$ecure#Pass`

---

### ☐ 2. Configure HTTPS for Admin Panel

**Priority:** 🔴 CRITICAL

**Why:** Prevents man-in-the-middle attacks and credential theft.

**Steps:**

#### Option A: Using Nginx (Recommended)

**Install Certbot (Let's Encrypt):**
```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

**Obtain SSL Certificate:**
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

**Nginx Configuration:**
```nginx
# /etc/nginx/sites-available/student-platform

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Admin Panel - Extra Security
    location /admin {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Optional: IP Whitelist
        # allow 203.0.113.0/24;  # Your office IP range
        # deny all;
    }

    # API Backend
    location /api {
        proxy_pass http://localhost:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Test Configuration:**
```bash
sudo nginx -t
sudo systemctl reload nginx
```

**Auto-Renewal:**
```bash
sudo certbot renew --dry-run
```

#### Option B: Using Cloudflare (Easiest)

1. Sign up at https://cloudflare.com
2. Add your domain
3. Update nameservers
4. Enable "Always Use HTTPS" in SSL/TLS settings
5. Set SSL/TLS encryption mode to "Full (strict)"

---

### ☐ 3. Implement Rate Limiting on Admin API

**Priority:** 🟠 HIGH

**Why:** Prevents brute-force attacks and DDoS.

**Implementation:**

#### Install slowapi (FastAPI Rate Limiting)
```bash
pip install slowapi
```

#### Update `backend/main.py`:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Initialize limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

#### Update `backend/routers/admin.py`:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Apply rate limiting to admin endpoints
@router.get("/stats/overview")
@limiter.limit("30/minute")  # Max 30 requests per minute
async def get_stats_overview(
    request: Request,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    # ... existing code

@router.get("/users")
@limiter.limit("60/minute")  # Max 60 requests per minute
async def get_users(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    search: str = None,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    # ... existing code

# Stricter limit for login
@router.post("/auth/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute
async def admin_login(request: Request, credentials: dict):
    # ... existing code
```

**Rate Limit Recommendations:**
- **Login:** 5 requests/minute
- **Read Operations:** 60 requests/minute
- **Write Operations:** 30 requests/minute
- **Settings Updates:** 10 requests/minute

---

### ☐ 4. Implement Audit Logging for Admin Actions

**Priority:** 🟠 HIGH

**Why:** Track who did what and when for security and compliance.

**Implementation:**

#### Create Audit Log Model:
```python
# backend/main.py

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)  # e.g., "USER_BLOCKED", "SETTINGS_UPDATED"
    resource_type = Column(String)  # e.g., "user", "settings"
    resource_id = Column(Integer, nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String)
    user_agent = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")
```

#### Create Migration:
```bash
# Create tables
python -c "from main import engine, Base; Base.metadata.create_all(bind=engine)"
```

#### Add Logging Helper:
```python
# backend/utils/audit.py

from sqlalchemy.orm import Session
from main import AuditLog
from datetime import datetime

def log_admin_action(
    db: Session,
    user_id: int,
    action: str,
    resource_type: str,
    resource_id: int = None,
    details: dict = None,
    ip_address: str = None,
    user_agent: str = None
):
    """Log admin action to audit log"""
    log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent,
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()
```

#### Use in Admin Routes:
```python
# backend/routers/admin.py

from utils.audit import log_admin_action

@router.put("/users/{user_id}/status")
async def update_user_status(
    request: Request,
    user_id: int,
    status_update: dict,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    old_status = user.is_active
    user.is_active = status_update.get("is_active", user.is_active)
    db.commit()
    
    # Log the action
    log_admin_action(
        db=db,
        user_id=current_user.id,
        action="USER_STATUS_CHANGED",
        resource_type="user",
        resource_id=user_id,
        details={
            "old_status": old_status,
            "new_status": user.is_active,
            "target_user_email": user.email
        },
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    return {"message": "User status updated"}
```

**Actions to Log:**
- ✅ User login/logout
- ✅ User block/unblock
- ✅ Settings changes
- ✅ Data exports
- ✅ Failed login attempts

---

### ☐ 5. Database Backup Strategy

**Priority:** 🔴 CRITICAL

**Why:** Protect against data loss from hardware failure, attacks, or human error.

**Implementation:**

#### Automated Daily Backups:

**Create Backup Script:**
```bash
#!/bin/bash
# /opt/scripts/backup_database.sh

# Configuration
DB_NAME="student_platform"
DB_USER="postgres"
BACKUP_DIR="/var/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory
mkdir -p $BACKUP_DIR

# Perform backup
pg_dump -U $DB_USER -d $DB_NAME | gzip > $BACKUP_DIR/backup_${DATE}.sql.gz

# Delete old backups
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

# Upload to S3 (optional)
# aws s3 cp $BACKUP_DIR/backup_${DATE}.sql.gz s3://your-bucket/backups/

echo "Backup completed: backup_${DATE}.sql.gz"
```

**Make Executable:**
```bash
chmod +x /opt/scripts/backup_database.sh
```

**Schedule with Cron:**
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /opt/scripts/backup_database.sh >> /var/log/db_backup.log 2>&1
```

#### Manual Backup:
```bash
# Full database backup
pg_dump -U postgres student_platform > backup_$(date +%Y%m%d).sql

# Compressed backup
pg_dump -U postgres student_platform | gzip > backup_$(date +%Y%m%d).sql.gz
```

#### Restore from Backup:
```bash
# Decompress
gunzip backup_20260211.sql.gz

# Restore
psql -U postgres student_platform < backup_20260211.sql
```

**Backup Locations:**
- ✅ Local server (daily)
- ✅ Cloud storage (S3, Google Cloud Storage)
- ✅ Off-site location (different data center)

---

### ☐ 6. Monitor Admin Activity

**Priority:** 🟡 MEDIUM

**Why:** Detect suspicious behavior and security incidents early.

**Implementation:**

#### Option A: Using Sentry (Recommended)

**Install:**
```bash
pip install sentry-sdk[fastapi]
npm install @sentry/nextjs
```

**Backend Setup:**
```python
# backend/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
    environment="production"
)
```

**Frontend Setup:**
```javascript
// frontend/sentry.client.config.js
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: "your-sentry-dsn",
  environment: "production",
  tracesSampleRate: 1.0,
});
```

#### Option B: Custom Monitoring

**Create Monitoring Endpoint:**
```python
# backend/routers/admin.py

@router.get("/monitoring/activity")
async def get_admin_activity(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get recent admin activity for monitoring"""
    recent_logs = db.query(AuditLog)\
        .order_by(AuditLog.timestamp.desc())\
        .limit(100)\
        .all()
    
    return {
        "total_actions": len(recent_logs),
        "actions": [
            {
                "user": log.user.email,
                "action": log.action,
                "timestamp": log.timestamp,
                "ip": log.ip_address
            }
            for log in recent_logs
        ]
    }
```

**Alerts to Set Up:**
- 🚨 Multiple failed login attempts
- 🚨 Admin actions outside business hours
- 🚨 Bulk user modifications
- 🚨 Settings changes
- 🚨 Database errors

---

### ☐ 7. Configure Security Headers

**Priority:** 🟠 HIGH

**Why:** Protect against XSS, clickjacking, and other web vulnerabilities.

**Implementation:**

#### Update Backend (FastAPI):
```python
# backend/main.py

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Prevent clickjacking
    response.headers["X-Frame-Options"] = "DENY"
    
    # Prevent MIME sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    
    # XSS Protection
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # Content Security Policy
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self' https://api.openai.com"
    )
    
    # Strict Transport Security (HTTPS only)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    # Referrer Policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Permissions Policy
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    return response

# Trusted Host
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourdomain.com", "www.yourdomain.com", "localhost"]
)
```

#### Update Frontend (Next.js):
```javascript
// frontend/next.config.js

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=31536000; includeSubDomains',
          },
        ],
      },
    ];
  },
};
```

---

### ☐ 8. Configure CORS Properly

**Priority:** 🟠 HIGH

**Why:** Prevent unauthorized cross-origin requests.

**Implementation:**

#### Production CORS Settings:
```python
# backend/main.py

# DEVELOPMENT (Current - Too Permissive!)
# origins = ["*"]  # ❌ NEVER use in production!

# PRODUCTION (Secure)
origins = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
    # Add other trusted domains only
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specific domains only
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Specific methods
    allow_headers=["Authorization", "Content-Type"],  # Specific headers
    max_age=3600,  # Cache preflight requests for 1 hour
)
```

**Environment-Based Configuration:**
```python
# backend/main.py
import os

# Get environment
ENV = os.getenv("ENVIRONMENT", "development")

if ENV == "production":
    origins = [
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ]
else:
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

---

## Additional Security Measures

### ☐ 9. Environment Variables Security

**Priority:** 🟠 HIGH

**Never commit `.env` files to Git!**

**Create `.env.example`:**
```bash
# .env.example
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=sk-your-key-here
ENVIRONMENT=production
```

**Add to `.gitignore`:**
```
.env
.env.local
.env.production
```

**Use Secret Management:**
- AWS Secrets Manager
- HashiCorp Vault
- Google Secret Manager

---

### ☐ 10. IP Whitelisting (Optional)

**Priority:** 🟡 MEDIUM

**Restrict admin access to specific IPs:**

```nginx
# Nginx configuration
location /admin {
    # Allow specific IPs
    allow 203.0.113.10;  # Office IP
    allow 203.0.113.20;  # VPN IP
    deny all;
    
    proxy_pass http://localhost:3000;
}
```

---

### ☐ 11. Two-Factor Authentication (Future)

**Priority:** 🟡 MEDIUM

**Recommended libraries:**
- `pyotp` (Python)
- `speakeasy` (Node.js)

---

## Deployment Checklist Summary

Before going live, verify:

- [ ] ✅ Default admin password changed
- [ ] ✅ HTTPS configured and working
- [ ] ✅ Rate limiting implemented
- [ ] ✅ Audit logging active
- [ ] ✅ Database backups scheduled
- [ ] ✅ Monitoring/alerting set up
- [ ] ✅ Security headers configured
- [ ] ✅ CORS properly restricted
- [ ] ✅ Environment variables secured
- [ ] ✅ `.env` not in Git
- [ ] ✅ Error messages don't leak sensitive info
- [ ] ✅ Admin panel tested on production
- [ ] ✅ Backup restore tested
- [ ] ✅ Team trained on admin panel

---

## Post-Deployment

### Regular Maintenance

**Weekly:**
- Review audit logs for suspicious activity
- Check backup integrity

**Monthly:**
- Update dependencies (`npm audit fix`, `pip list --outdated`)
- Review and rotate API keys
- Test backup restoration

**Quarterly:**
- Security audit
- Penetration testing
- Review access permissions

---

## Emergency Procedures

### If Admin Account Compromised:

1. **Immediately disable account:**
   ```sql
   UPDATE users SET is_active = false WHERE email = 'compromised@email.com';
   ```

2. **Review audit logs:**
   ```sql
   SELECT * FROM audit_logs WHERE user_id = X ORDER BY timestamp DESC;
   ```

3. **Change all passwords**
4. **Rotate JWT secret key**
5. **Investigate breach source**

### If Database Compromised:

1. **Take system offline**
2. **Restore from last known good backup**
3. **Investigate breach**
4. **Notify affected users (if required by law)**

---

## Support & Resources

**Documentation:**
- Admin Panel Guide: `ADMIN_PANEL_GUIDE.md`
- Testing Checklist: `ADMIN_TESTING_CHECKLIST.md`

**Security Resources:**
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
- Next.js Security: https://nextjs.org/docs/advanced-features/security-headers

---

**End of Production Checklist**

*Last updated: February 11, 2026*
