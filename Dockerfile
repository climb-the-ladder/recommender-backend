FROM python:3.9

WORKDIR /app

# Install git for cloning repositories
RUN apt-get update && apt-get install -y git

# The repository URL will be passed as a build argument
ARG RECOMMENDER_DATA_REPO=https://github.com/climb-the-ladder/recommender-data.git
ARG RECOMMENDER_MODELS_REPO=https://github.com/climb-the-ladder/recommender-models.git
ARG RECOMMENDER_AI_REPO=https://github.com/climb-the-ladder/recommender-ai.git

# Clone the recommender-ai repository
RUN git clone ${RECOMMENDER_DATA_REPO} /recommender-data
RUN git clone ${RECOMMENDER_MODELS_REPO} /recommender-models
RUN git clone ${RECOMMENDER_AI_REPO} /recommender-ai

# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN if [ -f /recommender-ai/requirements.txt ]; then pip install --no-cache-dir -r /recommender-ai/requirements.txt; fi

ENV PORT=5000
EXPOSE $PORT

CMD ["python", "app.py"]
