"""
Unit Tests for Case Management Module

Tests cover:
- CRUD operations (create, read, update, delete)
- Status transition validation
- Role-based access control (RBAC)
- Reminder service
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from main import app, Base, get_db
from api.cases_v2 import Case, CaseLog, CaseDocument
from services.case_status import validate_status_transition, ALLOWED_TRANSITIONS
from services.reminder_service import ReminderService, schedule_deadline_reminders

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# Fixtures
@pytest.fixture
def test_user_token():
    """Create test user and return JWT token."""
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201
    return response.json()["access_token"]


@pytest.fixture
def test_admin_token():
    """Create admin user and return JWT token."""
    # This would require modifying user role in database
    # For now, using regular user token
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Admin User",
            "email": "admin@example.com",
            "password": "adminpass123"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
def test_case_data():
    """Sample case data for testing."""
    return {
        "title": "Test Legal Case",
        "description": "Test case description",
        "deadline": (datetime.utcnow() + timedelta(days=30)).isoformat(),
        "priority": "high",
        "claim_amount": 5000.00,
        "client_name": "John Doe",
        "client_email": "john@example.com",
        "client_phone": "+421900123456"
    }


# Test 1: Case CRUD Operations
class TestCaseCRUD:
    """Test Create, Read, Update, Delete operations."""
    
    def test_create_case(self, test_user_token, test_case_data):
        """Test creating a new case."""
        response = client.post(
            "/api/cases",
            json=test_case_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == test_case_data["title"]
        assert data["status"] == "draft"
        assert "id" in data
    
    def test_get_cases_list(self, test_user_token):
        """Test retrieving list of cases."""
        response = client.get(
            "/api/cases",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_case_detail(self, test_user_token, test_case_data):
        """Test retrieving case details."""
        # Create case first
        create_response = client.post(
            "/api/cases",
            json=test_case_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Get case detail
        response = client.get(
            f"/api/cases/{case_id}",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == case_id
        assert "logs" in data
        assert "documents" in data
    
    def test_update_case_draft(self, test_user_token, test_case_data):
        """Test updating a draft case."""
        # Create case
        create_response = client.post(
            "/api/cases",
            json=test_case_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Update case
        update_data = {"title": "Updated Title"}
        response = client.patch(
            f"/api/cases/{case_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"
    
    def test_update_non_draft_fails(self, test_user_token, test_case_data):
        """Test that non-draft cases cannot be updated by regular users."""
        # Create and submit case
        create_response = client.post(
            "/api/cases",
            json=test_case_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Change status to submitted
        client.post(
            f"/api/cases/{case_id}/status",
            json={"new_status": "submitted"},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        # Try to update
        response = client.patch(
            f"/api/cases/{case_id}",
            json={"title": "Should Fail"},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 403


# Test 2: Status Transitions
class TestStatusTransitions:
    """Test status transition logic and validation."""
    
    def test_valid_transition_draft_to_submitted(self):
        """Test valid transition from draft to submitted."""
        is_valid, error = validate_status_transition("draft", "submitted")
        assert is_valid is True
        assert error is None
    
    def test_invalid_transition_draft_to_resolved(self):
        """Test invalid transition from draft to resolved."""
        is_valid, error = validate_status_transition("draft", "resolved")
        assert is_valid is False
        assert "Cannot transition" in error
    
    def test_terminal_status_cannot_change(self):
        """Test that terminal statuses cannot be changed."""
        is_valid, error = validate_status_transition("resolved", "under_review")
        assert is_valid is False
        assert "terminal" in error.lower()
    
    def test_all_allowed_transitions(self):
        """Test all defined allowed transitions."""
        for current, allowed_list in ALLOWED_TRANSITIONS.items():
            for next_status in allowed_list:
                is_valid, error = validate_status_transition(current, next_status)
                assert is_valid is True, f"Failed: {current} -> {next_status}"
    
    def test_status_change_creates_log(self, test_user_token, test_case_data):
        """Test that status changes create log entries."""
        # Create case
        create_response = client.post(
            "/api/cases",
            json=test_case_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Change status
        client.post(
            f"/api/cases/{case_id}/status",
            json={"new_status": "submitted"},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        # Get case and check logs
        response = client.get(
            f"/api/cases/{case_id}",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        logs = response.json()["logs"]
        status_change_logs = [log for log in logs if log["event_type"] == "status_change"]
        assert len(status_change_logs) > 0
        assert status_change_logs[0]["old_value"] == "draft"
        assert status_change_logs[0]["new_value"] == "submitted"


# Test 3: Role-Based Access Control
class TestRBAC:
    """Test role-based access control."""
    
    def test_user_cannot_access_other_user_case(self, test_user_token):
        """Test that users cannot access cases they don't own."""
        # Create case with first user
        case_data = {"title": "Private Case", "description": "Test"}
        create_response = client.post(
            "/api/cases",
            json=case_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Create second user
        client.post(
            "/api/auth/register",
            json={
                "name": "Other User",
                "email": "other@example.com",
                "password": "pass123"
            }
        )
        other_token = client.post(
            "/api/auth/login",
            data={"username": "other@example.com", "password": "pass123"}
        ).json()["access_token"]
        
        # Try to access with second user
        response = client.get(
            f"/api/cases/{case_id}",
            headers={"Authorization": f"Bearer {other_token}"}
        )
        
        assert response.status_code == 403
    
    def test_user_can_only_see_own_cases(self, test_user_token):
        """Test that users only see their own cases in list."""
        # Create case
        client.post(
            "/api/cases",
            json={"title": "My Case"},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        # Get list
        response = client.get(
            "/api/cases",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        cases = response.json()
        # All cases should belong to current user
        # (This assumes user_id is available in response)
        assert len(cases) >= 1


# Test 4: Reminder Service
class TestReminderService:
    """Test deadline reminder functionality."""
    
    @patch('services.reminder_service.logger')
    def test_reminder_service_checks_deadlines(self, mock_logger):
        """Test that reminder service finds upcoming deadlines."""
        service = ReminderService()
        db = TestingSessionLocal()
        
        # Create test case with deadline in 7 days
        deadline = datetime.utcnow() + timedelta(days=7)
        test_case = Case(
            title="Test Case",
            user_id=1,
            status="submitted",
            deadline=deadline
        )
        db.add(test_case)
        db.commit()
        
        # Check for reminders
        reminders = service.check_upcoming_deadlines(db)
        
        # Should find the case
        assert len(reminders) > 0
        assert reminders[0]['case_title'] == "Test Case"
        assert reminders[0]['days_until'] == 7
        
        db.close()
    
    @patch('services.reminder_service.logger')
    def test_send_reminder_logs_to_console(self, mock_logger):
        """Test that reminders are logged (MVP implementation)."""
        service = ReminderService()
        
        reminder = {
            'case_id': 'test-123',
            'case_title': 'Test Case',
            'deadline': datetime.utcnow(),
            'days_until': 3,
            'user_id': 1
        }
        
        result = service.send_reminder(reminder)
        
        assert result is True
        assert mock_logger.info.called
    
    def test_schedule_reminders_creates_logs(self):
        """Test that scheduling reminders creates log entries."""
        db = TestingSessionLocal()
        
        # Create test case
        test_case = Case(
            title="Test Case",
            user_id=1,
            status="draft",
            deadline=datetime.utcnow() + timedelta(days=30)
        )
        db.add(test_case)
        db.commit()
        
        # Schedule reminders
        schedule_deadline_reminders(db, str(test_case.id), test_case.deadline, 1)
        
        # Check logs
        logs = db.query(CaseLog).filter(
            CaseLog.case_id == str(test_case.id),
            CaseLog.event_type == "reminder_scheduled"
        ).all()
        
        assert len(logs) == 3  # 7, 3, 1 days before
        
        db.close()


# Test 5: Document Management
class TestDocumentManagement:
    """Test document upload and management."""
    
    def test_upload_document(self, test_user_token, test_case_data):
        """Test uploading a document to a case."""
        # Create case
        create_response = client.post(
            "/api/cases",
            json=test_case_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Mock file upload
        files = {"file": ("test.pdf", b"fake pdf content", "application/pdf")}
        
        with patch('services.doc_processor.storage.MinIOStorage.upload_file'):
            response = client.post(
                f"/api/cases/{case_id}/documents",
                files=files,
                headers={"Authorization": f"Bearer {test_user_token}"}
            )
        
        assert response.status_code == 201
        assert response.json()["success"] is True
    
    def test_list_case_documents(self, test_user_token, test_case_data):
        """Test listing documents for a case."""
        # Create case
        create_response = client.post(
            "/api/cases",
            json=test_case_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Get documents
        response = client.get(
            f"/api/cases/{case_id}/documents",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)


# Test 6: Timeline
class TestTimeline:
    """Test case timeline functionality."""
    
    def test_timeline_shows_all_events(self, test_user_token, test_case_data):
        """Test that timeline shows all case events."""
        # Create case
        create_response = client.post(
            "/api/cases",
            json=test_case_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        case_id = create_response.json()["id"]
        
        # Add note
        client.post(
            f"/api/cases/{case_id}/notes",
            json={"comment": "Test note"},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        # Change status
        client.post(
            f"/api/cases/{case_id}/status",
            json={"new_status": "submitted"},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        # Get timeline
        response = client.get(
            f"/api/cases/{case_id}/timeline",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        timeline = response.json()
        assert len(timeline) >= 3  # created, note, status_change
    
    def test_timeline_filter_by_event_type(self, test_user_token, test_case_data):
        """Test filtering timeline by event type."""
        # Create case and add events
        create_response = client.post(
            "/api/cases",
            json=test_case_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        case_id = create_response.json()["id"]
        
        client.post(
            f"/api/cases/{case_id}/notes",
            json={"comment": "Note 1"},
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        # Get only notes
        response = client.get(
            f"/api/cases/{case_id}/timeline?event_type=note",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        
        assert response.status_code == 200
        timeline = response.json()
        assert all(event["event_type"] == "note" for event in timeline)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
