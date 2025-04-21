# Testing in a Multi-Repository Project

This document explains how testing works in our multi-repository project structure.

## Project Structure

Our project is split across multiple repositories:

- **recommender-backend**: Flask API (this repository)
- **recommender-ai**: AI models and chatbot functionality
- **recommender-frontend**: User interface
- **recommender-data**: Data processing and storage

## Testing Approach

Since the backend depends on modules from other repositories (specifically the AI repository), we've implemented a testing strategy that uses mocks to isolate the backend tests.

### How It Works

1. **Mock External Dependencies**: In `conftest.py` and `run_tests.py`, we mock the modules from other repositories using Python's `unittest.mock` library.

2. **Custom Test Runner**: The `run_tests.py` script sets up all necessary mocks before running the tests, making it easy to run tests with a single command.

3. **Modular Tests**: Each test file focuses on testing a specific component of the backend, using mocks for external dependencies.

4. **CI/CD Integration**: The GitHub Actions workflow is configured to use the custom test runner, ensuring tests can run without access to the other repositories.

## Running Tests

### Using Mocks (Recommended for Local Development)

```
python run_tests.py
```

This runs all tests with mocked dependencies, so you don't need access to other repositories.

### Using Actual Dependencies

If you want to test with actual implementations:

1. Clone all related repositories in the same parent directory:
   ```
   parent-directory/
   ├── recommender-backend/
   ├── recommender-ai/
   └── ...
   ```

2. Add the repositories to your PYTHONPATH:
   ```
   export PYTHONPATH=$PYTHONPATH:../recommender-ai
   ```

3. Modify `conftest.py` to import actual modules instead of mocks.

## Common Issues and Solutions

### ModuleNotFoundError

If you see `ModuleNotFoundError: No module named 'chatbot'` or similar errors, it means:

1. You're trying to run tests without using the test runner script, or
2. The mocking setup in `conftest.py` is not working correctly

**Solution**: Use `python run_tests.py` to run tests, which ensures all dependencies are properly mocked.

### Test Failures Due to Missing Mock Functionality

If tests fail with errors like `AttributeError: 'MagicMock' object has no attribute 'X'`, it means:

1. The mock object doesn't have all the necessary methods or attributes
2. The patch is not applied correctly

**Solution**: Update the mocks in `conftest.py` to include all necessary attributes and methods.

## Adding New Tests

When adding new tests:

1. Use `pytest` fixtures from `conftest.py`
2. Prefer `monkeypatch` over `patch` decorators for mocking when possible
3. Update mocks in `conftest.py` if you need to mock new external dependencies 