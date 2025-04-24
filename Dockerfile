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

# Copy application files
COPY . .

# Install dependencies before model training
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
RUN if [ -f recommender-ai/requirements.txt ]; then pip install --no-cache-dir -r recommender-ai/requirements.txt; fi

# Verify the processed data exists
RUN echo "=== Checking for processed data ==="
RUN ls -la recommender-data/processed/ || echo "Processed data directory not found"
RUN if [ -f recommender-data/processed/processed_dataset.csv ]; then echo "✅ Found processed dataset"; else echo "❌ Processed dataset not found"; fi

# Run the training script to generate models during build
WORKDIR /app/recommender-models
RUN echo "Starting model training..."

# Run the train_model.py file from the cloned recommender-models repository 
RUN python train_model.py
RUN echo "Model training completed."

# Return to app directory
WORKDIR /app

# Verify the models were created
RUN echo "=== Checking model files ==="
RUN ls -la recommender-models/*.pkl || echo "No model files found"

# Add AI code to Python path
ENV PYTHONPATH="${PYTHONPATH}:/app:/app/recommender-ai"

# Port will be provided by Render as an environment variable
EXPOSE 8080

# Use gunicorn to start the application
CMD gunicorn --bind 0.0.0.0:8080 app:app
