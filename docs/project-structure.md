# 🧱 Backend Project Structure

```
recommender-backend/
├── app.py                 # Main Flask application entry point
├── routes/               # API route handlers
│   ├── __init__.py
│   ├── recommendations.py # Career prediction and details endpoints
│   ├── chatbot.py        # Chatbot and university recommendation endpoints
│   └── users.py          # User management endpoints (future)
├── database/            # Database related files
│   ├── schema.sql       # Database schema
│   └── seed_data.py     # Initial data population
├── recommender-ai/      # AI model integration
│   ├── chatbot.py       # Career chatbot implementation
│   └── gpt_chatbot.py   # GPT-based chat handling
├── recommender-models/  # ML models and training
│   └── train_model.py   # Model training script
├── recommender-data/    # Data processing and storage
│   └── processed/       # Processed datasets
├── tests/              # Unit and integration tests
├── docs/               # Project documentation
│   ├── api-reference.md
│   └── project-structure.md
├── .env.example        # Environment variables template
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
├── docker-compose.yml # Multi-container setup
├── Procfile          # Process manager configuration
└── runtime.txt       # Python runtime version
```

## Purpose
This backend serves as the API layer for the Climb The Ladder system, providing:

1. **Career Prediction**
   - ML-based career recommendations
   - Detailed career information
   - Career development roadmaps

2. **AI Chatbot**
   - Career guidance conversations
   - University recommendations
   - Similar career suggestions

3. **Data Management**
   - User data storage
   - Career information database
   - Model training and updates

## Key Components

### Routes
- `recommendations.py`: Handles career predictions and detailed information
- `chatbot.py`: Manages AI chatbot interactions and university recommendations
- `users.py`: (Future) User management and authentication

### AI Integration
- `recommender-ai/`: Contains AI model integration code
- `recommender-models/`: Stores trained ML models
- `recommender-data/`: Houses processed datasets

### Infrastructure
- Docker configuration for containerization
- Environment variable management
- Process management with Procfile
- Database schema and seeding

## Development Setup
1. Clone the repository
2. Copy `.env.example` to `.env` and configure variables
3. Install dependencies: `pip install -r requirements.txt`
4. Run the development server: `python app.py`

## Deployment
The application is containerized using Docker and can be deployed using:
- Docker Compose for local development
- Container platforms (e.g., Heroku, AWS) for production 