FROM python:3.9

WORKDIR /app

# Install git for cloning repositories and supervisor for process management
RUN apt-get update && apt-get install -y git supervisor

# The repository URL will be passed as a build argument
ARG RECOMMENDER_DATA_REPO=https://github.com/climb-the-ladder/recommender-data.git
ARG RECOMMENDER_MODELS_REPO=https://github.com/climb-the-ladder/recommender-models.git
ARG RECOMMENDER_AI_REPO=https://github.com/climb-the-ladder/recommender-ai.git

# Clone the recommender-ai repository
RUN git clone ${RECOMMENDER_DATA_REPO} /recommender-data
RUN git clone ${RECOMMENDER_MODELS_REPO} /recommender-models
RUN git clone ${RECOMMENDER_AI_REPO} /recommender-ai

# Fix paths in AI files for data access
RUN sed -i 's|recommender-data/raw|/recommender-data/raw|g' /recommender-ai/chatbot.py
RUN sed -i 's|../recommender-data/raw|/recommender-data/raw|g' /recommender-ai/chatbot.py
RUN sed -i 's|recommender-data/raw|/recommender-data/raw|g' /recommender-ai/gpt_chatbot.py
RUN sed -i 's|../recommender-data/raw|/recommender-data/raw|g' /recommender-ai/gpt_chatbot.py
RUN sed -i 's|recommender-models/|/recommender-models/|g' /recommender-ai/app.py
RUN sed -i 's|../recommender-models/|/recommender-models/|g' /recommender-ai/app.py

# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
RUN if [ -f /recommender-ai/requirements.txt ]; then pip install --no-cache-dir -r /recommender-ai/requirements.txt; fi

# Add AI code to Python path
ENV PYTHONPATH="${PYTHONPATH}:/recommender-ai"

# Set up supervisor configuration
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create the supervisor config if it doesn't exist
RUN echo "[supervisord]" > /etc/supervisor/conf.d/supervisord.conf && \
    echo "nodaemon=true" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "[program:backend]" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "command=gunicorn --bind 0.0.0.0:8080 app:app" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "directory=/app" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "autostart=true" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "autorestart=true" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "stdout_logfile=/dev/stdout" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "stdout_logfile_maxbytes=0" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "stderr_logfile=/dev/stderr" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "stderr_logfile_maxbytes=0" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "[program:ai]" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "command=python app.py" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "directory=/recommender-ai" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "autostart=true" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "autorestart=true" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "stdout_logfile=/dev/stdout" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "stdout_logfile_maxbytes=0" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "stderr_logfile=/dev/stderr" >> /etc/supervisor/conf.d/supervisord.conf && \
    echo "stderr_logfile_maxbytes=0" >> /etc/supervisor/conf.d/supervisord.conf

# Port will be provided by Render as an environment variable
EXPOSE 8080 5001

# Start supervisor which will run both the backend and AI services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
