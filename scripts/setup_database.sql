-- Create initial database tables
-- This will be handled by Django migrations, but here's the SQL structure

-- Study Materials table
CREATE TABLE IF NOT EXISTS core_studymaterial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    content_type VARCHAR(20) NOT NULL,
    file VARCHAR(100),
    youtube_url VARCHAR(200),
    raw_content TEXT NOT NULL,
    summary TEXT,
    created_at DATETIME NOT NULL,
    user_id INTEGER
);

-- Flashcards table
CREATE TABLE IF NOT EXISTS core_flashcard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_material_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    difficulty VARCHAR(20) DEFAULT 'medium',
    created_at DATETIME NOT NULL,
    FOREIGN KEY (study_material_id) REFERENCES core_studymaterial (id)
);

-- Quizzes table
CREATE TABLE IF NOT EXISTS core_quiz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_material_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    questions_data TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (study_material_id) REFERENCES core_studymaterial (id)
);

-- Chat Messages table
CREATE TABLE IF NOT EXISTS core_chatmessage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_material_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (study_material_id) REFERENCES core_studymaterial (id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_studymaterial_content_type ON core_studymaterial(content_type);
CREATE INDEX IF NOT EXISTS idx_studymaterial_created_at ON core_studymaterial(created_at);
CREATE INDEX IF NOT EXISTS idx_flashcard_difficulty ON core_flashcard(difficulty);
CREATE INDEX IF NOT EXISTS idx_chatmessage_created_at ON core_chatmessage(created_at);
