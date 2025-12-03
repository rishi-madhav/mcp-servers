"""
StudyBuddy MCP Server - Enhanced Educational Tools
Production-ready MCP server for Indian students (Grades 5-10)
Supports CBSE, ICSE, and IGCSE curricula
"""

import asyncio
import json
import sqlite3
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

# FastMCP imports
from fastmcp import FastMCP

# Gemini imports
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY not found in environment variables")
    raise ValueError("GEMINI_API_KEY is required")

genai.configure(api_key=GEMINI_API_KEY)

# Try different Gemini models in order of preference
MODEL_CANDIDATES = [
    "models/gemini-2.0-flash-exp",
    "models/gemini-1.5-flash",
    "models/gemini-pro"
]

def get_best_model():
    """Get the best available Gemini model"""
    try:
        available_models = [m.name for m in genai.list_models() 
                          if 'generateContent' in m.supported_generation_methods]
        
        for model in MODEL_CANDIDATES:
            if model in available_models:
                logger.info(f"Using Gemini model: {model}")
                return model
        
        # Fallback
        logger.warning("No preferred models found, using default")
        return "models/gemini-1.5-flash"
        
    except Exception as e:
        logger.error(f"Error checking models: {e}")
        return "models/gemini-1.5-flash"

GEMINI_MODEL = get_best_model()

# Database setup
DB_PATH = Path("studybuddy_data.db")

def init_database():
    """Initialize SQLite database for tracking learning progress"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # User profiles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade INTEGER NOT NULL,
            board TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Learning activities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            activity_type TEXT NOT NULL,
            topic TEXT NOT NULL,
            subject TEXT NOT NULL,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_profiles (id)
        )
    ''')
    
    # Quiz history table for preventing duplicates
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            topic TEXT NOT NULL,
            question_hash TEXT NOT NULL,
            question_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_profiles (id)
        )
    ''')
    
    # Progress tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT NOT NULL,
            topics_learned INTEGER DEFAULT 0,
            problems_solved INTEGER DEFAULT 0,
            quizzes_completed INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_profiles (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

# Initialize database on startup
init_database()

# Initialize FastMCP server
app = FastMCP("StudyBuddy Educational Assistant")

# ============================================
# UTILITY FUNCTIONS
# ============================================

def call_gemini(prompt: str, max_retries: int = 3) -> str:
    """Call Gemini API with retry logic"""
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel(GEMINI_MODEL)
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2048,
                )
            )
            return response.text
        except Exception as e:
            logger.warning(f"Gemini API attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
    return ""

def validate_json_response(response: str) -> Dict[str, Any]:
    """Validate and parse JSON response from Gemini"""
    try:
        # Clean response - remove markdown code blocks if present
        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        logger.error(f"Raw response: {response}")
        raise ValueError("Invalid JSON response from AI")

def get_user_id(name: str, grade: int, board: str) -> int:
    """Get or create user profile and return user_id"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute(
        "SELECT id FROM user_profiles WHERE name = ? AND grade = ? AND board = ?",
        (name, grade, board)
    )
    result = cursor.fetchone()
    
    if result:
        user_id = result[0]
        # Update last active
        cursor.execute(
            "UPDATE user_profiles SET last_active = CURRENT_TIMESTAMP WHERE id = ?",
            (user_id,)
        )
    else:
        # Create new user
        cursor.execute(
            "INSERT INTO user_profiles (name, grade, board) VALUES (?, ?, ?)",
            (name, grade, board)
        )
        user_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return user_id

def log_activity(user_id: int, activity_type: str, topic: str, subject: str, content: str):
    """Log learning activity to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO learning_activities (user_id, activity_type, topic, subject, content) VALUES (?, ?, ?, ?, ?)",
        (user_id, activity_type, topic, subject, json.dumps(content))
    )
    
    conn.commit()
    conn.close()

def get_previous_quiz_questions(user_id: int, topic: str) -> List[str]:
    """Get previously asked quiz questions for a user and topic"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT question_text FROM quiz_questions WHERE user_id = ? AND topic = ? ORDER BY created_at DESC LIMIT 50",
        (user_id, topic)
    )
    
    results = cursor.fetchall()
    conn.close()
    
    return [row[0] for row in results]

def store_quiz_questions(user_id: int, topic: str, questions: List[str]):
    """Store quiz questions to prevent future duplicates"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for question in questions:
        question_hash = str(hash(question))
        cursor.execute(
            "INSERT OR IGNORE INTO quiz_questions (user_id, topic, question_hash, question_text) VALUES (?, ?, ?, ?)",
            (user_id, topic, question_hash, question)
        )
    
    conn.commit()
    conn.close()

# ============================================
# PROMPT TEMPLATES
# ============================================

def get_explain_prompt(topic: str, subject: str, grade: int, board: str) -> str:
    """Generate prompt for topic explanation"""
    return f"""You are an expert {board} teacher explaining {subject} concepts to grade {grade} students.

Topic to explain: "{topic}"

Create a comprehensive yet age-appropriate explanation that:
1. Uses simple, clear language for grade {grade} level
2. Follows {board} curriculum standards
3. Includes real-world examples students can relate to
4. Breaks down complex concepts into digestible parts
5. Engages with Indian context and examples where relevant

Respond ONLY with a JSON object in this exact format:
{{
    "topic": "{topic}",
    "subject": "{subject}",
    "grade": {grade},
    "board": "{board}",
    "explanation": "detailed explanation in simple language",
    "key_points": ["point 1", "point 2", "point 3"],
    "real_world_example": "relatable example",
    "fun_fact": "interesting related fact",
    "next_topics": ["related topic 1", "related topic 2"]
}}

DO NOT include any text outside the JSON structure."""

def get_practice_prompt(topic: str, subject: str, grade: int, board: str, num_questions: int) -> str:
    """Generate prompt for practice problems"""
    return f"""You are creating practice problems for a grade {grade} {board} student studying {subject}.

Topic: "{topic}"

Generate exactly {num_questions} practice problems that:
1. Match {board} exam style and difficulty for grade {grade}
2. Progress from easier to harder
3. Test different aspects of {topic}
4. Include variety in problem types
5. Have clear, step-by-step solutions

Respond ONLY with a JSON object in this exact format:
{{
    "topic": "{topic}",
    "subject": "{subject}",
    "grade": {grade},
    "board": "{board}",
    "problems": [
        {{
            "problem_number": 1,
            "question": "the problem statement",
            "difficulty": "easy|medium|hard",
            "solution": "step-by-step solution",
            "answer": "final answer",
            "concept_tested": "specific concept"
        }}
    ]
}}

Generate exactly {num_questions} problems. DO NOT include any text outside the JSON structure."""

def get_solve_prompt(problem: str, subject: str, grade: int) -> str:
    """Generate prompt for step-by-step problem solving"""
    return f"""You are a patient {subject} teacher helping a grade {grade} student solve a problem step-by-step.

Problem: "{problem}"

Provide a detailed solution that:
1. Identifies what type of problem this is
2. Lists the given information
3. Shows each step clearly with explanations
4. Explains the reasoning behind each step
5. Provides the final answer
6. Suggests how to check the answer

Respond ONLY with a JSON object in this exact format:
{{
    "problem": "{problem}",
    "subject": "{subject}",
    "grade": {grade},
    "problem_type": "type of problem",
    "given_information": ["fact 1", "fact 2"],
    "steps": [
        {{
            "step_number": 1,
            "description": "what we're doing in this step",
            "work": "the actual calculation or reasoning",
            "result": "result of this step"
        }}
    ],
    "final_answer": "the complete final answer",
    "verification": "how to check if the answer is correct",
    "key_concept": "main concept demonstrated"
}}

DO NOT include any text outside the JSON structure."""

def get_story_prompt(topic: str, subject: str, grade: int) -> str:
    """Generate prompt for educational stories"""
    return f"""You are a creative educator transforming {subject} concepts into engaging stories for grade {grade} students.

Topic: "{topic}"

Create an entertaining story that:
1. Features relatable characters (kids, animals, or fantasy characters)
2. Naturally incorporates key concepts of {topic}
3. Has a clear beginning, middle, and end with conflict resolution
4. Makes learning memorable and fun
5. Uses vocabulary appropriate for grade {grade}
6. Length: 400-600 words

Respond ONLY with a JSON object in this exact format:
{{
    "topic": "{topic}",
    "subject": "{subject}",
    "grade": {grade},
    "story_title": "catchy, engaging title",
    "story": "the complete story text",
    "main_characters": ["character 1", "character 2"],
    "key_concepts_taught": ["concept 1", "concept 2"],
    "discussion_questions": ["question 1", "question 2"],
    "moral_lesson": "what students learn beyond the academic content"
}}

DO NOT include any text outside the JSON structure."""

def get_quiz_prompt(topic: str, subject: str, grade: int, board: str, previous_questions: List[str]) -> str:
    """Generate prompt for quiz questions"""
    prev_q_text = ""
    if previous_questions:
        prev_q_text = f"\n\nIMPORTANT: Do NOT repeat these previously asked questions:\n" + "\n".join(
            f"- {q}" for q in previous_questions[-30:]  # Last 30 questions to avoid
        )
    
    return f"""You are creating a comprehensive quiz for a grade {grade} {board} student on {subject}.

Topic: "{topic}"

Generate exactly 10 unique quiz questions that:
1. Follow {board} exam patterns and difficulty for grade {grade}
2. Mix question types: 4 MCQ, 3 True/False, 3 Short Answer
3. Have varied difficulty: 3 easy, 4 medium, 3 hard
4. Test different aspects of {topic}
5. Encourage critical thinking, not just memorization{prev_q_text}

Respond ONLY with a JSON object in this exact format:
{{
    "topic": "{topic}",
    "subject": "{subject}",
    "grade": {grade},
    "board": "{board}",
    "questions": [
        {{
            "question_number": 1,
            "question": "the question text",
            "type": "mcq|true_false|short_answer",
            "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
            "correct_answer": "the correct answer",
            "explanation": "detailed explanation of why this is correct",
            "difficulty": "easy|medium|hard",
            "concept": "specific concept being tested"
        }}
    ],
    "total_questions": 10,
    "estimated_time": "time in minutes to complete"
}}

For True/False questions, use options: ["True", "False"]
For Short Answer questions, use options: []
Generate exactly 10 unique questions. DO NOT include any text outside the JSON structure."""

# ============================================
# MCP TOOLS
# ============================================

@app.tool()
async def studybuddy_explain_topic(
    topic: str,
    subject: str,
    grade: int,
    board: str,
    student_name: str = "Student"
) -> str:
    """
    Explain any topic at grade-appropriate level aligned with CBSE/ICSE/IGCSE curricula.
    
    Args:
        topic: The topic to explain
        subject: Subject name (e.g., Mathematics, Science, English)
        grade: Grade level (5-10)
        board: Education board (CBSE, ICSE, IGCSE)
        student_name: Student's name for personalization
    """
    try:
        # Validate inputs
        if not topic or not subject:
            raise ValueError("Topic and subject are required")
        
        if grade < 5 or grade > 10:
            raise ValueError("Grade must be between 5 and 10")
        
        if board not in ["CBSE", "ICSE", "IGCSE"]:
            raise ValueError("Board must be CBSE, ICSE, or IGCSE")
        
        # Get user ID and log activity
        user_id = get_user_id(student_name, grade, board)
        
        # Generate explanation
        prompt = get_explain_prompt(topic, subject, grade, board)
        response = call_gemini(prompt)
        
        # Validate and parse JSON
        result = validate_json_response(response)
        
        # Log activity
        log_activity(user_id, "explanation", topic, subject, result)
        
        logger.info(f"Explained topic '{topic}' for {student_name} (Grade {grade}, {board})")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error explaining topic: {e}")
        return json.dumps({
            "error": str(e),
            "topic": topic,
            "message": "Failed to generate explanation. Please try again."
        })

@app.tool()
async def studybuddy_generate_practice(
    topic: str,
    subject: str,
    grade: int,
    board: str,
    num_questions: int = 5,
    student_name: str = "Student"
) -> str:
    """
    Generate practice questions for any topic with solutions.
    
    Args:
        topic: The topic for practice problems
        subject: Subject name
        grade: Grade level (5-10)
        board: Education board (CBSE, ICSE, IGCSE)
        num_questions: Number of questions to generate (1-10)
        student_name: Student's name for tracking
    """
    try:
        # Validate inputs
        if not topic or not subject:
            raise ValueError("Topic and subject are required")
        
        if grade < 5 or grade > 10:
            raise ValueError("Grade must be between 5 and 10")
        
        if board not in ["CBSE", "ICSE", "IGCSE"]:
            raise ValueError("Board must be CBSE, ICSE, or IGCSE")
        
        if num_questions < 1 or num_questions > 10:
            raise ValueError("Number of questions must be between 1 and 10")
        
        # Get user ID
        user_id = get_user_id(student_name, grade, board)
        
        # Generate practice problems
        prompt = get_practice_prompt(topic, subject, grade, board, num_questions)
        response = call_gemini(prompt)
        
        # Validate and parse JSON
        result = validate_json_response(response)
        
        # Log activity
        log_activity(user_id, "practice_problems", topic, subject, result)
        
        logger.info(f"Generated {num_questions} practice problems for '{topic}' - {student_name}")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error generating practice problems: {e}")
        return json.dumps({
            "error": str(e),
            "topic": topic,
            "message": "Failed to generate practice problems. Please try again."
        })

@app.tool()
async def studybuddy_solve_step_by_step(
    problem: str,
    subject: str,
    grade: int,
    student_name: str = "Student"
) -> str:
    """
    Solve math/science problems with detailed step-by-step explanations.
    
    Args:
        problem: The complete problem statement to solve
        subject: Subject (typically Mathematics or Science)
        grade: Grade level (5-10)
        student_name: Student's name for tracking
    """
    try:
        # Validate inputs
        if not problem or not subject:
            raise ValueError("Problem statement and subject are required")
        
        if grade < 5 or grade > 10:
            raise ValueError("Grade must be between 5 and 10")
        
        # Get user ID
        user_id = get_user_id(student_name, grade, "GENERAL")
        
        # Generate step-by-step solution
        prompt = get_solve_prompt(problem, subject, grade)
        response = call_gemini(prompt)
        
        # Validate and parse JSON
        result = validate_json_response(response)
        
        # Log activity
        log_activity(user_id, "problem_solved", f"Problem: {problem[:50]}...", subject, result)
        
        logger.info(f"Solved problem for {student_name} (Grade {grade})")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error solving problem: {e}")
        return json.dumps({
            "error": str(e),
            "problem": problem,
            "message": "Failed to solve problem. Please try again."
        })

@app.tool()
async def studybuddy_create_story(
    topic: str,
    subject: str,
    grade: int,
    student_name: str = "Student"
) -> str:
    """
    Turn boring topics into fun, engaging stories with characters and plot.
    
    Args:
        topic: The educational topic to turn into a story
        subject: Subject name
        grade: Grade level (5-10)
        student_name: Student's name for tracking
    """
    try:
        # Validate inputs
        if not topic or not subject:
            raise ValueError("Topic and subject are required")
        
        if grade < 5 or grade > 10:
            raise ValueError("Grade must be between 5 and 10")
        
        # Get user ID
        user_id = get_user_id(student_name, grade, "GENERAL")
        
        # Generate educational story
        prompt = get_story_prompt(topic, subject, grade)
        response = call_gemini(prompt)
        
        # Validate and parse JSON
        result = validate_json_response(response)
        
        # Log activity
        log_activity(user_id, "story_created", topic, subject, result)
        
        logger.info(f"Created story for '{topic}' - {student_name} (Grade {grade})")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error creating story: {e}")
        return json.dumps({
            "error": str(e),
            "topic": topic,
            "message": "Failed to create story. Please try again."
        })

@app.tool()
async def studybuddy_quiz_me(
    topic: str,
    subject: str,
    grade: int,
    board: str,
    student_name: str = "Student"
) -> str:
    """
    Generate a 10-question quiz on any topic with intelligent question tracking.
    
    Args:
        topic: The topic for the quiz
        subject: Subject name
        grade: Grade level (5-10)
        board: Education board (CBSE, ICSE, IGCSE)
        student_name: Student's name for tracking
    """
    try:
        # Validate inputs
        if not topic or not subject:
            raise ValueError("Topic and subject are required")
        
        if grade < 5 or grade > 10:
            raise ValueError("Grade must be between 5 and 10")
        
        if board not in ["CBSE", "ICSE", "IGCSE"]:
            raise ValueError("Board must be CBSE, ICSE, or IGCSE")
        
        # Get user ID
        user_id = get_user_id(student_name, grade, board)
        
        # Get previous questions to avoid duplicates
        previous_questions = get_previous_quiz_questions(user_id, topic)
        
        # Generate quiz
        prompt = get_quiz_prompt(topic, subject, grade, board, previous_questions)
        response = call_gemini(prompt)
        
        # Validate and parse JSON
        result = validate_json_response(response)
        
        # Store new questions to prevent future duplicates
        if "questions" in result:
            new_questions = [q["question"] for q in result["questions"]]
            store_quiz_questions(user_id, topic, new_questions)
        
        # Log activity
        log_activity(user_id, "quiz_completed", topic, subject, result)
        
        logger.info(f"Generated quiz for '{topic}' - {student_name} (avoided {len(previous_questions)} previous questions)")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
        return json.dumps({
            "error": str(e),
            "topic": topic,
            "message": "Failed to generate quiz. Please try again."
        })

@app.tool()
async def studybuddy_get_progress(student_name: str = "Student") -> str:
    """
    Get learning progress and history for a student.
    
    Args:
        student_name: Student's name
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get all user profiles for this name
        cursor.execute(
            "SELECT id, grade, board, created_at FROM user_profiles WHERE name = ? ORDER BY last_active DESC",
            (student_name,)
        )
        profiles = cursor.fetchall()
        
        if not profiles:
            return json.dumps({
                "student_name": student_name,
                "message": "No learning history found. Start using StudyBuddy tools to build your progress!",
                "profiles": []
            })
        
        progress_data = {
            "student_name": student_name,
            "profiles": []
        }
        
        for profile_id, grade, board, created_at in profiles:
            # Get activity counts
            cursor.execute(
                "SELECT activity_type, COUNT(*) FROM learning_activities WHERE user_id = ? GROUP BY activity_type",
                (profile_id,)
            )
            activity_counts = dict(cursor.fetchall())
            
            # Get recent activities
            cursor.execute(
                "SELECT activity_type, topic, subject, created_at FROM learning_activities WHERE user_id = ? ORDER BY created_at DESC LIMIT 10",
                (profile_id,)
            )
            recent_activities = cursor.fetchall()
            
            profile_data = {
                "grade": grade,
                "board": board,
                "started_on": created_at,
                "activity_summary": {
                    "explanations": activity_counts.get("explanation", 0),
                    "practice_problems": activity_counts.get("practice_problems", 0),
                    "problems_solved": activity_counts.get("problem_solved", 0),
                    "stories_created": activity_counts.get("story_created", 0),
                    "quizzes_completed": activity_counts.get("quiz_completed", 0)
                },
                "recent_activities": [
                    {
                        "type": activity_type,
                        "topic": topic,
                        "subject": subject,
                        "date": created_at
                    }
                    for activity_type, topic, subject, created_at in recent_activities
                ]
            }
            
            progress_data["profiles"].append(profile_data)
        
        conn.close()
        
        logger.info(f"Retrieved progress for {student_name}")
        return json.dumps(progress_data, indent=2)
        
    except Exception as e:
        logger.error(f"Error getting progress: {e}")
        return json.dumps({
            "error": str(e),
            "student_name": student_name,
            "message": "Failed to retrieve progress. Please try again."
        })

# ============================================
# SERVER STARTUP
# ============================================

if __name__ == "__main__":
    logger.info("Starting StudyBuddy MCP Server...")
    logger.info(f"Database: {DB_PATH}")
    logger.info(f"Gemini Model: {GEMINI_MODEL}")
    
    # Run the FastMCP server
    app.run()
