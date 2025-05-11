# Testing the Recommender Backend

This directory contains tests for the recommender-backend application. The tests use pytest and are designed to be run locally or in a CI/CD pipeline.

## Multi-Repository Structure

This project is part of a multi-repository system, where different components are stored in different repositories:
- recommender-backend (this repo)
- recommender-ai
- recommender-frontend
- recommender-data

The tests in this directory use mocks to handle dependencies on other repositories, so you don't need to have all repositories available to run the tests.

## Running Tests Locally

To run the tests locally, follow these steps:

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   pip install -r test-requirements.txt
   ```

2. Run the tests using the helper script (recommended):
   ```
   python run_tests.py
   ```

   This script sets up the necessary mocks for dependencies in other repositories.

3. Or run the tests directly with pytest (requires manual setup):
   ```
   pytest -v tests/
   ```

4. To generate a test coverage report:
   ```
   coverage run -m pytest tests/
   coverage report
   ```

## Using Actual Dependencies Instead of Mocks

If you want to test with actual implementations instead of mocks:

1. Clone the related repositories in a shared parent directory:
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

3. Modify conftest.py to import the actual modules instead of creating mocks.

## CI/CD Integration

The tests are automatically run on every pull request to the `main` or `master` branch using GitHub Actions. The workflow is defined in `.github/workflows/python-tests.yml`.

The CI/CD pipeline will:
1. Set up a Python environment
2. Install dependencies
3. Set up mocks for external dependencies
4. Run the tests
5. Generate and upload a test coverage report

## Adding New Tests

When adding new features or endpoints to the API, please add corresponding tests. Tests should:

1. Be placed in the `tests/` directory
2. Follow the pytest style (functions with assertions)
3. Use fixtures from `conftest.py` where appropriate
4. Mock external dependencies to ensure tests are isolated

## Test Structure

- `test_app.py`: Tests for the basic Flask application setup
- `test_recommendations.py`: Tests for the recommendation endpoints
- `test_chatbot.py`: Tests for the chatbot endpoints 