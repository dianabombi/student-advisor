# Authentication Module Documentation

## Overview

The CODEX platform includes a comprehensive authentication and authorization system implementing JWT-based authentication, role-based access control (RBAC), and secure session management.

## Features

### 🔐 Authentication
- **User Registration**: Create new accounts with email/password
- **Login**: JWT token generation with user profile
- **Password Security**: Bcrypt hashing with automatic salt
- **Token Expiration**: Configurable token lifetime (default: 30 minutes)
- **Profile Management**: View and update user information

### 👥 Authorization (RBAC)
- **Three Roles**: User, Partner Lawyer, Admin
- **Route Protection**: Middleware-based access control
- **Endpoint Guards**: Decorator-based role verification
- **Permission System**: Fine-grained permission management

### 📋 Case Management
- **Create Cases**: Users can create legal cases
- **Draft Support**: JSON-based draft data storage
- **Ownership**: Users can only access their own cases
- **Admin Override**: Admins can view all cases

## API Endpoints

### Authentication Endpoints

**Base URL**: `/api/auth`

#### POST /register
Register a new user account.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "user@example.com",
    "role": "user",
    "is_active": true,
    "is_verified": false
  }
}
```

#### POST /login
Login and receive JWT token.

**Request Body (form-data):**
```
username=user@example.com
password=securePassword123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "user@example.com",
    "role": "user"
  }
}
```

#### GET /profile
Get current user profile (requires authentication).

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "user@example.com",
  "role": "user",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-12-04T20:00:00"
}
```

### Cases Endpoints

**Base URL**: `/api/cases`

#### GET /cases
List user's cases.

**Query Parameters:**
- `user_id`: (Admin only) Filter by user ID
- `status`: Filter by status (draft, active, closed, archived)

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Case Title",
    "description": "Case description",
    "status": "active",
    "case_type": "civil",
    "created_at": "2024-12-04T20:00:00"
  }
]
```

#### POST /cases
Create a new case.

**Request Body:**
```json
{
  "title": "New Case",
  "description": "Case description",
  "case_type": "civil",
  "draft_data": {
    "plaintiff": "John Doe",
    "defendant": "Jane Smith"
  }
}
```

#### PATCH /cases/{id}
Update case or save draft.

**Request Body:**
```json
{
  "draft_data": {
    "plaintiff": "Updated Name",
    "evidence": ["Document 1", "Document 2"]
  }
}
```

## User Roles

### User (default)
- Create and manage own cases
- Upload documents
- Use AI chat
- View own profile

### Partner Lawyer
- All user permissions
- View assigned cases
- Manage templates
- Access consultation dashboard

### Admin
- All permissions
- User management
- System configuration
- View all cases
- Access admin dashboard

## Environment Variables

Required environment variables in `.env`:

```env
# Authentication
SECRET_KEY=your-secret-key-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

## Security Best Practices

### Password Security
- Minimum 8 characters recommended
- Bcrypt hashing with automatic salt
- Password verification constant-time comparison

### Token Security
- JWT signed with HS256 algorithm
- Configurable expiration time
- Role and permissions in token payload
- Store tokens securely (localStorage/cookies)

### API Security
- All sensitive endpoints require authentication
- Role-based access control enforced
- CORS configured for allowed origins
- Rate limiting recommended for production

## Testing

### Run Unit Tests
```bash
docker compose exec backend pytest tests/test_auth.py -v
```

### Run Integration Tests
```bash
docker compose exec backend pytest tests/test_integration_auth.py -v
```

### Test Coverage
- Password hashing: 7 tests
- JWT tokens: 9 tests
- Registration: 4 tests
- Login: 4 tests
- Protected endpoints: 5 tests
- RBAC: 3 tests
- Complete flows: 2 tests

**Total: 36 tests**

## Database Migration

Apply authentication tables:

```bash
# Copy migration file to container
docker cp backend/migrations/001_add_auth_tables.sql codex-db:/tmp/

# Run migration
docker compose exec db psql -U postgres -d codex_db -f /tmp/001_add_auth_tables.sql
```

## Frontend Integration

### useAuth Hook
```typescript
import { useAuth } from '@/contexts/AuthContext';

function MyComponent() {
  const { user, login, logout, isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <LoginPage />;
  }
  
  return <div>Welcome {user.name}!</div>;
}
```

### Protected Routes
```typescript
import { withAuth } from '@/contexts/AuthContext';

function AdminPage() {
  return <div>Admin Dashboard</div>;
}

export default withAuth(AdminPage, { adminOnly: true });
```

### Role-Based Rendering
```typescript
import { AdminOnly, LawyerOnly } from '@/components/RoleGuard';

<AdminOnly>
  <button>Delete User</button>
</AdminOnly>

<LawyerOnly>
  <div>Consultation Panel</div>
</LawyerOnly>
```

## API Documentation

Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Troubleshooting

### Token Expired
**Error**: 401 Unauthorized  
**Solution**: Refresh token or login again

### Invalid Credentials
**Error**: 401 Incorrect email or password  
**Solution**: Verify email/password, check database

### Permission Denied
**Error**: 403 Forbidden  
**Solution**: User doesn't have required role

### Database Connection
**Error**: Could not connect to database  
**Solution**: Verify DATABASE_URL in .env
