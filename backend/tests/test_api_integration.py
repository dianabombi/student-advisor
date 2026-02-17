"""
Integration tests for Document Processing API

Tests the complete pipeline: upload → processing → results
Validates HTTP codes and response structures.
"""

import pytest
import time
import io
from pathlib import Path
from fastapi.testclient import TestClient

# Import the FastAPI app
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import app

# Test client
client = TestClient(app)

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / 'test_data'


@pytest.fixture
def auth_token():
    """Get authentication token for tests."""
    # Register test user
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    
    # Login to get token
    response = client.post(
        "/api/auth/login",
        data={
            "username": "test@example.com",
            "password": "testpass123"
        }
    )
    
    if response.status_code == 200:
        return response.json()["access_token"]
    
    # If user already exists, just login
    return response.json().get("access_token")


@pytest.fixture
def admin_token():
    """Get admin authentication token."""
    # This would require creating admin user
    # For now, use regular token
    return auth_token()


class TestDocumentUploadAPI:
    """Tests for document upload endpoint."""
    
    def test_upload_without_auth(self):
        """Test upload without authentication."""
        response = client.post(
            "/api/documents/upload",
            files={"file": ("test.txt", b"test content", "text/plain")}
        )
        
        assert response.status_code == 401  # Unauthorized
    
    def test_upload_valid_pdf(self, auth_token):
        """Test uploading valid PDF file."""
        file_content = b"%PDF-1.4\ntest content"
        
        response = client.post(
            "/api/documents/upload",
            headers={"Authorization": f"Bearer {auth_token}"},
            files={"file": ("test.pdf", file_content, "application/pdf")},
            data={"auto_process": "true"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "success" in data
        assert data["success"] is True
        assert "document_id" in data
        assert "message" in data
        assert "status" in data
        assert data["status"] in ["pending", "processing"]
    
    def test_upload_invalid_file_type(self, auth_token):
        """Test uploading unsupported file type."""
        response = client.post(
            "/api/documents/upload",
            headers={"Authorization": f"Bearer {auth_token}"},
            files={"file": ("test.exe", b"executable", "application/exe")}
        )
        
        assert response.status_code == 400  # Bad Request
        data = response.json()
        assert "detail" in data
    
    def test_upload_file_size_display(self, auth_token):
        """Test that file size is properly handled."""
        large_content = b"x" * (1024 * 1024)  # 1MB
        
        response = client.post(
            "/api/documents/upload",
            headers={"Authorization": f"Bearer {auth_token}"},
            files={"file": ("large.pdf", large_content, "application/pdf")}
        )
        
        # Should accept if within limits
        assert response.status_code in [200, 413]  # OK or Payload Too Large


class TestDocumentProcessingPipeline:
    """Tests for complete processing pipeline."""
    
    def test_full_pipeline_employment_contract(self, auth_token):
        """Test complete pipeline with employment contract."""
        # Step 1: Upload document
        contract_text = """
        PRACOVNÁ ZMLUVA č. ZML-001/2024
        uzavretá dňa 15.12.2024
        
        Zamestnávateľ: ABC s.r.o.
        IČO: 12345678
        
        Zamestnanec: Ján Novák
        Pracovná pozícia: Programátor
        Mzda: 2000 EUR
        """
        
        upload_response = client.post(
            "/api/documents/upload",
            headers={"Authorization": f"Bearer {auth_token}"},
            files={"file": ("contract.txt", contract_text.encode(), "text/plain")},
            data={"auto_process": "true"}
        )
        
        assert upload_response.status_code == 200
        document_id = upload_response.json()["document_id"]
        
        # Step 2: Poll for status
        max_retries = 30
        for i in range(max_retries):
            time.sleep(2)  # Wait 2 seconds
            
            status_response = client.get(
                f"/api/documents/{document_id}/status",
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            
            assert status_response.status_code == 200
            status_data = status_response.json()
            
            # Validate status structure
            assert "document_id" in status_data
            assert "status" in status_data
            assert "progress" in status_data
            assert 0 <= status_data["progress"] <= 100
            
            if status_data["status"] == "completed":
                break
            elif status_data["status"] == "failed":
                pytest.fail(f"Processing failed: {status_data}")
        
        # Step 3: Get full result
        result_response = client.get(
            f"/api/documents/{document_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert result_response.status_code == 200
        result = result_response.json()
        
        # Validate result structure
        assert "document_id" in result
        assert "filename" in result
        assert "status" in result
        assert result["status"] == "completed"
        
        # Validate classification
        if "document_type" in result:
            assert result["document_type"] == "employment_contract"
        
        # Validate extracted fields
        if "extracted_fields" in result:
            fields = result["extracted_fields"]
            # Should have some fields extracted
            assert isinstance(fields, dict)
    
    def test_full_pipeline_invoice(self, auth_token):
        """Test complete pipeline with invoice."""
        invoice_text = """
        FAKTÚRA č. FA-123/2024
        
        Dátum vystavenia: 15.12.2024
        Dodávateľ: XYZ s.r.o.
        IČO: 87654321
        DIČ: SK2020123456
        
        Suma celkom: 1500.00 EUR
        """
        
        # Upload
        upload_response = client.post(
            "/api/documents/upload",
            headers={"Authorization": f"Bearer {auth_token}"},
            files={"file": ("invoice.txt", invoice_text.encode(), "text/plain")},
            data={"auto_process": "true"}
        )
        
        assert upload_response.status_code == 200
        document_id = upload_response.json()["document_id"]
        
        # Wait for processing
        time.sleep(5)
        
        # Get result
        result_response = client.get(
            f"/api/documents/{document_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert result_response.status_code == 200


class TestDocumentListingAPI:
    """Tests for document listing endpoint."""
    
    def test_list_documents_without_auth(self):
        """Test listing without authentication."""
        response = client.get("/api/documents/")
        
        assert response.status_code == 401
    
    def test_list_documents_with_auth(self, auth_token):
        """Test listing user's documents."""
        response = client.get(
            "/api/documents/",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return list
        assert isinstance(data, list)
    
    def test_list_documents_with_filter(self, auth_token):
        """Test listing with status filter."""
        response = client.get(
            "/api/documents/?status=completed",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # All should have completed status
        for doc in data:
            assert doc["status"] == "completed"


class TestDocumentDeletionAPI:
    """Tests for document deletion endpoint."""
    
    def test_delete_without_auth(self):
        """Test deletion without authentication."""
        response = client.delete("/api/documents/test-id")
        
        assert response.status_code == 401
    
    def test_delete_nonexistent_document(self, auth_token):
        """Test deleting non-existent document."""
        response = client.delete(
            "/api/documents/nonexistent-id",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 404
    
    def test_delete_own_document(self, auth_token):
        """Test deleting own document."""
        # First upload a document
        upload_response = client.post(
            "/api/documents/upload",
            headers={"Authorization": f"Bearer {auth_token}"},
            files={"file": ("test.txt", b"test", "text/plain")}
        )
        
        document_id = upload_response.json()["document_id"]
        
        # Then delete it
        delete_response = client.delete(
            f"/api/documents/{document_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert delete_response.status_code == 200
        data = delete_response.json()
        assert data["success"] is True


class TestTemplateManagementAPI:
    """Tests for template management endpoints."""
    
    def test_list_templates_without_auth(self):
        """Test listing templates without auth."""
        response = client.get("/api/templates/")
        
        assert response.status_code == 401
    
    def test_upload_template_without_admin(self, auth_token):
        """Test uploading template without admin role."""
        response = client.post(
            "/api/templates/upload",
            headers={"Authorization": f"Bearer {auth_token}"},
            files={"file": ("template.docx", b"content", "application/docx")}
        )
        
        # Should require admin
        assert response.status_code in [401, 403]
    
    def test_list_templates_with_admin(self, admin_token):
        """Test listing templates with admin."""
        response = client.get(
            "/api/templates/",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        # Admin should be able to list
        assert response.status_code == 200
        data = response.json()
        assert "templates" in data
        assert "total" in data


class TestResponseStructures:
    """Tests for API response structures."""
    
    def test_error_response_structure(self):
        """Test that errors have consistent structure."""
        response = client.get("/api/documents/")
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
    
    def test_success_response_structure(self, auth_token):
        """Test that success responses are consistent."""
        response = client.get(
            "/api/documents/",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 200
        # Should return valid JSON
        assert response.json() is not None


class TestHTTPStatusCodes:
    """Tests for proper HTTP status codes."""
    
    def test_200_ok(self, auth_token):
        """Test 200 OK responses."""
        response = client.get(
            "/api/documents/",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
    
    def test_401_unauthorized(self):
        """Test 401 Unauthorized responses."""
        response = client.get("/api/documents/")
        assert response.status_code == 401
    
    def test_404_not_found(self, auth_token):
        """Test 404 Not Found responses."""
        response = client.get(
            "/api/documents/nonexistent",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 404
    
    def test_400_bad_request(self, auth_token):
        """Test 400 Bad Request responses."""
        response = client.post(
            "/api/documents/upload",
            headers={"Authorization": f"Bearer {auth_token}"},
            files={"file": ("test.exe", b"exe", "application/exe")}
        )
        assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
