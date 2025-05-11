import pytest
from app import app as flask_app

def test_app_exists():
    assert flask_app is not None
    
def test_app_configuration():
    # Test that debug mode is enabled for development
    assert flask_app.config['DEBUG'] is True
    
def test_cors_enabled(client):
    # Test that CORS headers are present
    response = client.get('/', headers={'Origin': 'http://localhost:3000'})
    assert 'Access-Control-Allow-Origin' in response.headers

def test_not_found_handling(client):
    """Test that non-existent endpoints return 404"""
    response = client.get('/non-existent-endpoint')
    assert response.status_code == 404

if __name__ == '__main__':
    pytest.main() 