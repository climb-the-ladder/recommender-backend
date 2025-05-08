-- Drop existing table
DROP TABLE IF EXISTS student_activities;

-- Create updated student_activities table
CREATE TABLE student_activities (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    
    -- Study Habits
    preferred_study_time VARCHAR(50),
    study_environment VARCHAR(50),
    learning_style VARCHAR(50),
    study_methods TEXT,
    
    -- Skills & Strengths
    technical_skills VARCHAR(255)[],
    soft_skills VARCHAR(255)[],
    languages_spoken VARCHAR(255)[],
    
    -- Experiential Inputs
    extracurricular_activities TEXT,
    internship_experience TEXT,
    volunteer_experience TEXT,
    awards_recognitions TEXT,
    
    -- AI-Enhancing Fields
    career_motivation VARCHAR(50),
    open_to_abroad BOOLEAN,
    learning_preference VARCHAR(50),
    
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Create index
CREATE INDEX idx_student_activities_user_id ON student_activities(user_id);

-- Create RLS policy
CREATE POLICY "Users can view their own activities" ON student_activities
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own activities" ON student_activities
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own activities" ON student_activities
    FOR INSERT WITH CHECK (auth.uid() = user_id); 