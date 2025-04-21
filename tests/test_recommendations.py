import pytest
import json
from unittest.mock import patch, MagicMock
from app import app

@patch('routes.recommendations.requests.post')
def test_get_prediction(mock_post, client):
    # Mock the AI service response
    mock_response = MagicMock()
    mock_response.json.return_value = {"predicted_career": "Software Engineer"}
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    # Test data
    test_data = {
        "gpa": 3.8,
        "interests": ["coding", "problem solving"]
    }

    # Send request to the app
    response = client.post('/api/predict', 
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["predicted_career"] == "Software Engineer"
    
    # Verify the mock was called with correct data
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert kwargs['json'] == test_data

@patch('routes.recommendations.requests.post')
def test_get_prediction_ai_service_error(mock_post, client):
    # Mock the AI service failing
    mock_post.side_effect = Exception("AI service unavailable")
    
    # Test data
    test_data = {
        "gpa": 3.8,
        "interests": ["coding", "problem solving"]
    }
    
    # Send request to the app
    response = client.post('/api/predict', 
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    # Check response - should return error 500
    assert response.status_code == 500
    data = json.loads(response.data)
    assert "error" in data

if __name__ == '__main__':
    pytest.main()
