-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE academic_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE student_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE career_recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE career_roadmaps ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE university_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- Create users table
CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    gender VARCHAR(10),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create academic_scores table
CREATE TABLE academic_scores (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    math_score INTEGER,
    history_score INTEGER,
    physics_score INTEGER,
    chemistry_score INTEGER,
    biology_score INTEGER,
    english_score INTEGER,
    geography_score INTEGER,
    gpa DECIMAL(3,2),
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create student_activities table
CREATE TABLE student_activities (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    part_time_job BOOLEAN,
    absence_days INTEGER,
    extracurricular_activities BOOLEAN,
    weekly_self_study_hours INTEGER,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create career_recommendations table
CREATE TABLE career_recommendations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    recommended_career VARCHAR(255),
    confidence_score DECIMAL(5,4),
    recommended_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create career_roadmaps table
CREATE TABLE career_roadmaps (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    career VARCHAR(255),
    roadmap_steps JSONB,
    current_step INTEGER,
    completed_steps INTEGER[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create chat_history table
CREATE TABLE chat_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id VARCHAR(255),
    message TEXT,
    response TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create university_preferences table
CREATE TABLE university_preferences (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    preferred_universities VARCHAR(255)[],
    preferred_locations VARCHAR(255)[],
    budget_range VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create user_preferences table
CREATE TABLE user_preferences (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    preferred_career_fields VARCHAR(255)[],
    preferred_work_environment VARCHAR(255)[],
    salary_expectations VARCHAR(50),
    work_life_balance_preference VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_academic_scores_user_id ON academic_scores(user_id);
CREATE INDEX idx_student_activities_user_id ON student_activities(user_id);
CREATE INDEX idx_career_recommendations_user_id ON career_recommendations(user_id);
CREATE INDEX idx_career_roadmaps_user_id ON career_roadmaps(user_id);
CREATE INDEX idx_chat_history_user_id ON chat_history(user_id);
CREATE INDEX idx_university_preferences_user_id ON university_preferences(user_id);
CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);

-- Create RLS policies
CREATE POLICY "Users can view their own data" ON users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update their own data" ON users
    FOR UPDATE USING (auth.uid() = id);

-- Similar policies for other tables... 