FROM python:3.9

WORKDIR /app

# Install git for cloning repositories
RUN apt-get update && apt-get install -y git

# Clone the repositories
RUN git clone https://github.com/climb-the-ladder/recommender-data.git /recommender-data
RUN git clone https://github.com/climb-the-ladder/recommender-models.git /recommender-models
RUN git clone https://github.com/climb-the-ladder/recommender-ai.git /recommender-ai

# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r /recommender-ai/requirements.txt
RUN pip install gunicorn

ENV PORT=10000
EXPOSE $PORT

# Add AI code to Python path
ENV PYTHONPATH="${PYTHONPATH}:/recommender-ai"

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
