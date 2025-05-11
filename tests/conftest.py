import pytest
import sys
from unittest.mock import MagicMock

# Mock external dependencies before importing app
sys.modules['chatbot'] = MagicMock()
sys.modules['gpt_chatbot'] = MagicMock()

# Create a proper CareerChatbot mock with recommend method
career_chatbot_mock = MagicMock()
career_chatbot_mock.recommend = MagicMock(return_value=(["University A", "University B"], ["Career A", "Career B"]))
sys.modules['chatbot'].CareerChatbot = MagicMock(return_value=career_chatbot_mock)

# Mock the chat handler
sys.modules['gpt_chatbot'].handle_chat = MagicMock(return_value="This is a test response")

# Now we can safely import the app
from app import app as flask_app

# Set DEBUG to True for testing
flask_app.config['DEBUG'] = True

@pytest.fixture
def app():
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner() 