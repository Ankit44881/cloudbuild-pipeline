import pytest
from backend.app import app, is_valid_indian_phone

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Health check route test"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}

def test_indian_phone_validation():
    """Regex phone validation test"""
    assert is_valid_indian_phone("9876543210") == True
    assert is_valid_indian_phone("5876543210") == False  # Invalid starting digit
    assert is_valid_indian_phone("98765432") == False    # Less than 10 digits