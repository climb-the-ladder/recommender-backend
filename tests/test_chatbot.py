import pytest
import json
from unittest.mock import patch, MagicMock

@patch('routes.chatbot.handle_chat')
def test_chat(mock_handle_chat, client):
    # Mock the chat handler response
    mock_handle_chat.return_value = "This is a test response"

    # Test data
    test_data = {
        "message": "Tell me about computer science",
        "career": "Software Engineering",
        "gpa": 3.5,
        "subject_grades": {"math": "A", "physics": "B"},
        "session_id": "test-session"
    }

    # Send request to the app
    response = client.post('/api/chat', 
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["response"] == "This is a test response"
    
    # Verify the mock was called with correct data
    mock_handle_chat.assert_called_once_with(
        test_data["message"], 
        test_data["career"], 
        test_data["gpa"], 
        test_data["subject_grades"], 
        test_data["session_id"]
    )

def test_chatbot_recommend(client, monkeypatch):
    """
    Test for the chatbot recommend endpoint with monkeypatch instead of patch decorator.
    This avoids issues with patching a class that's imported from another repo.
    """
    # Test data
    test_data = {
        "gpa": 3.8,
        "career": "Computer Science"
    }

    # Create a mock for the career_chatbot instance used in the route
    from routes.chatbot import career_chatbot
    
    # Replace the recommend method on the instance with a mock
    mock_recommend = MagicMock()
    mock_recommend.return_value = (
        ["University A", "University B"], 
        ["Career A", "Career B"]
    )
    monkeypatch.setattr(career_chatbot, 'recommend', mock_recommend)

    # Send request to the app
    response = client.post('/api/chatbot-recommend', 
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["recommended_universities"] == ["University A", "University B"]
    assert data["similar_careers"] == ["Career A", "Career B"]
    
    # Verify the mock was called with correct data
    mock_recommend.assert_called_once_with(float(test_data["gpa"]), test_data["career"])

def test_chat_missing_message(client):
    """Test chat endpoint with missing message parameter"""
    # Test data missing the required message field
    test_data = {
        "career": "Software Engineering",
        "gpa": 3.5
    }
    
    # Send request to the app
    response = client.post('/api/chat', 
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    # Check response - should return 400 Bad Request
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

def test_chatbot_recommend_missing_fields(client):
    """Test chatbot recommend endpoint with missing required fields"""
    # Test with missing GPA
    response = client.post('/api/chatbot-recommend', 
                          data=json.dumps({"career": "Computer Science"}),
                          content_type='application/json')
    assert response.status_code == 400
    
    # Test with missing career
    response = client.post('/api/chatbot-recommend', 
                          data=json.dumps({"gpa": 3.5}),
                          content_type='application/json')
    assert response.status_code == 400 