#!/usr/bin/env python3
"""
Simple test runner script for the recommender-backend that handles
multi-repository dependencies by using mocks.
"""
import os
import sys
from unittest.mock import MagicMock

def setup_mock_dependencies():
    """
    Mock external dependencies from other repositories.
    """
    print("Setting up mock dependencies...")
    
    # Mock the imports from other repositories
    sys.modules['chatbot'] = MagicMock()
    sys.modules['gpt_chatbot'] = MagicMock()
    
    # Create a proper CareerChatbot mock with recommend method
    career_chatbot_mock = MagicMock()
    career_chatbot_mock.recommend = MagicMock(return_value=(["University A", "University B"], ["Career A", "Career B"]))
    sys.modules['chatbot'].CareerChatbot = MagicMock(return_value=career_chatbot_mock)
    
    # Mock the chat handler
    sys.modules['gpt_chatbot'].handle_chat = MagicMock(return_value="This is a test response")

def main():
    """
    Run the tests using pytest.
    """
    print("Running tests for recommender-backend...")
    
    # Set up mocks before importing pytest (which might trigger imports)
    setup_mock_dependencies()
    
    # Add project root to path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # Now it's safe to import pytest
    import pytest
    
    # Run tests
    exit_code = pytest.main(["-v", "tests/"])
    
    # Generate coverage report if tests pass
    if exit_code == 0:
        print("\nGenerating coverage report...")
        os.system("coverage run -m pytest tests/")
        os.system("coverage report")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main()) 