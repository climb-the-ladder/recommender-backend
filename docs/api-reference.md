# 📡 API Reference – Recommender Backend

## Base URL
http://localhost:8080/api

## Endpoints

### Career Prediction

#### `POST /predict`
- **Description:** Takes user input and returns career prediction(s)
- **Request Body:**
```json
{
  "math_score": 85,
  "history_score": 75,
  "physics_score": 90,
  "chemistry_score": 80,
  "biology_score": 85,
  "english_score": 88,
  "geography_score": 82
}
```
- **Response:**
```json
{
  "career": "Data Scientist"
}
```

### Career Details

#### `POST /career-details`
- **Description:** Returns detailed information about a specific career
- **Request Body:**
```json
{
  "career": "Data Scientist"
}
```
- **Response:**
```json
{
  "description": "Analyzes and interprets complex data to help organizations make better decisions.",
  "skills": ["Statistics", "Machine Learning", "Python/R", "Data Visualization"],
  "salary_range": "$90,000 - $160,000",
  "education": "Master's or PhD in Statistics, Computer Science, or related field",
  "difficulty": 8,
  "job_outlook": "Strong growth expected as businesses increasingly rely on data-driven decision making.",
  "day_to_day": "Analyzing data, building models, creating visualizations, presenting findings to stakeholders.",
  "advancement": "Can advance to senior data scientist, lead data scientist, or management positions.",
  "work_life_balance": {
    "rating": 8,
    "explanation": "Generally good work-life balance with flexible hours in many organizations."
  },
  "pros": ["Intellectually stimulating", "High demand", "Good compensation", "Opportunity to make business impact"],
  "cons": ["Requires extensive education", "Can be challenging to explain complex concepts", "May involve cleaning messy data"]
}
```

### Career Roadmap

#### `POST /career-roadmap`
- **Description:** Returns a detailed career development roadmap
- **Request Body:**
```json
{
  "career": "Data Scientist"
}
```
- **Response:**
```json
{
  "success": true,
  "data": {
    "short-term goals": [
      "Complete a bachelor's degree in a field related to Data Scientist",
      "Take relevant courses and gain foundational knowledge",
      "Build a portfolio of projects or work samples"
    ],
    "mid-term goals": [
      "Obtain entry-level position in the field",
      "Develop specialization in a particular area",
      "Build professional network through industry events"
    ],
    "long-term goals": [
      "Advance to senior-level positions",
      "Become a subject matter expert",
      "Consider leadership or management roles"
    ],
    "education requirements": [
      "Bachelor's degree in Data Scientist or related field",
      "Relevant certifications",
      "Continuing education to stay current"
    ],
    "skills to develop": [
      "Technical skills specific to the field",
      "Communication and teamwork",
      "Problem-solving and critical thinking"
    ],
    "experience needed": [
      "Entry-level positions or internships",
      "Volunteer work in related areas",
      "Collaborative projects"
    ],
    "industry certifications": [
      "Professional certifications relevant to the field",
      "Specialized training programs",
      "Online courses and workshops"
    ],
    "personal development recommendations": [
      "Develop time management skills",
      "Work on presentation and public speaking",
      "Build resilience and adaptability"
    ],
    "networking suggestions": [
      "Join professional associations",
      "Attend industry conferences",
      "Connect with professionals on LinkedIn"
    ],
    "milestones and checkpoints": [
      "First year: Complete foundational education",
      "3-5 years: Gain specialized experience",
      "5-10 years: Move into advanced roles"
    ]
  }
}
```

### Chatbot

#### `POST /chatbot-recommend`
- **Description:** Get university recommendations and similar careers based on GPA and career choice
- **Request Body:**
```json
{
  "gpa": 3.7,
  "career": "Data Scientist"
}
```
- **Response:**
```json
{
  "recommended_universities": ["University A", "University B"],
  "similar_careers": ["Career 1", "Career 2"]
}
```

#### `POST /chat`
- **Description:** Interact with the career guidance chatbot
- **Request Body:**
```json
{
  "message": "What skills do I need for data science?",
  "career": "Data Scientist",
  "gpa": 3.7,
  "subject_grades": {
    "math": 90,
    "programming": 85
  },
  "session_id": "user123"
}
```
- **Response:**
```json
{
  "response": "To succeed in data science, you'll need strong skills in statistics, programming (particularly Python or R), and data visualization..."
}
``` 