FROM python:3.9

WORKDIR /app

# Install git for cloning repositories
RUN apt-get update && apt-get install -y git

# The repository URL will be passed as a build argument
ARG RECOMMENDER_DATA_REPO=https://github.com/climb-the-ladder/recommender-data.git
ARG RECOMMENDER_MODELS_REPO=https://github.com/climb-the-ladder/recommender-models.git
ARG RECOMMENDER_AI_REPO=https://github.com/climb-the-ladder/recommender-ai.git

# Clone the recommender repositories into relative paths inside /app
RUN git clone ${RECOMMENDER_DATA_REPO} recommender-data
RUN git clone ${RECOMMENDER_MODELS_REPO} recommender-models
RUN git clone ${RECOMMENDER_AI_REPO} recommender-ai

# Verify if the model files exist
RUN ls -la recommender-models || echo "No models directory found"
RUN find recommender-models -type f -name "*.pkl" || echo "No PKL files found in models directory"

# Copy application files
COPY . .

# Verify file structure after copying
RUN echo "=== Checking final file structure ==="
RUN ls -la
RUN ls -la recommender-models || echo "Models directory not found"
RUN find . -name "*.pkl" || echo "No PKL files found"

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
RUN if [ -f recommender-ai/requirements.txt ]; then pip install --no-cache-dir -r recommender-ai/requirements.txt; fi

# Add AI code to Python path
ENV PYTHONPATH="${PYTHONPATH}:/app:/app/recommender-ai"

# Port will be provided by Render as an environment variable
EXPOSE 8080

# Use gunicorn to start the application
CMD gunicorn --bind 0.0.0.0:8080 app:app
