import aiosqlite
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

DB_PATH = Path(__file__).parent.parent / "data" / "studybuddy.db"

async def init_database():
    """Initialize the database with required tables."""
    DB_PATH.parent.mkdir(exist_ok=True)
    
    async with aiosqlite.connect(DB_PATH) as db:
        # Students table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                grade INTEGER CHECK(grade BETWEEN 5 AND 10),
                board TEXT CHECK(board IN ('CBSE', 'ICSE', 'IGCSE')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Explained topics table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS explained_topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject TEXT NOT NULL,
                topic TEXT NOT NULL,
                explanation TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
        """)
        
        # Practice problems table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS practice_problems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject TEXT NOT NULL,
                topic TEXT NOT NULL,
                problems TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
        """)
        
        # Quiz history table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS quiz_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject TEXT NOT NULL,
                topic TEXT NOT NULL,
                questions TEXT NOT NULL,
                score INTEGER,
                total_questions INTEGER DEFAULT 10,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
        """)
        
        await db.commit()

async def get_or_create_student(name: str, grade: int, board: str) -> int:
    """Get existing student ID or create new student."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Check if student exists
        async with db.execute(
            "SELECT id FROM students WHERE name = ? AND grade = ? AND board = ?",
            (name, grade, board)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]
        
        # Create new student
        await db.execute(
            "INSERT INTO students (name, grade, board) VALUES (?, ?, ?)",
            (name, grade, board)
        )
        await db.commit()
        
        async with db.execute("SELECT last_insert_rowid()") as cursor:
            row = await cursor.fetchone()
            return row[0]

async def save_explanation(student_id: int, subject: str, topic: str, explanation: str):
    """Save an explained topic."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO explained_topics (student_id, subject, topic, explanation) VALUES (?, ?, ?, ?)",
            (student_id, subject, topic, explanation)
        )
        await db.commit()

async def save_practice_problems(student_id: int, subject: str, topic: str, problems: List[Dict]):
    """Save generated practice problems."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO practice_problems (student_id, subject, topic, problems) VALUES (?, ?, ?, ?)",
            (student_id, subject, topic, json.dumps(problems))
        )
        await db.commit()

async def save_quiz_result(student_id: int, subject: str, topic: str, questions: List[Dict], score: int):
    """Save quiz history with score."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO quiz_history (student_id, subject, topic, questions, score) VALUES (?, ?, ?, ?, ?)",
            (student_id, subject, topic, json.dumps(questions), score)
        )
        await db.commit()

async def get_quiz_history(student_id: int, subject: str, topic: str) -> List[str]:
    """Get previously asked questions to avoid repeats."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT questions FROM quiz_history WHERE student_id = ? AND subject = ? AND topic = ?",
            (student_id, subject, topic)
        ) as cursor:
            rows = await cursor.fetchall()
            
            all_questions = []
            for row in rows:
                questions = json.loads(row[0])
                all_questions.extend([q["question"] for q in questions])
            
            return all_questions

async def get_student_history(student_id: int) -> Dict[str, Any]:
    """Get complete history for a student."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Get explained topics
        async with db.execute(
            "SELECT subject, topic, timestamp FROM explained_topics WHERE student_id = ? ORDER BY timestamp DESC LIMIT 10",
            (student_id,)
        ) as cursor:
            explained = await cursor.fetchall()
        
        # Get practice problems
        async with db.execute(
            "SELECT subject, topic, timestamp FROM practice_problems WHERE student_id = ? ORDER BY timestamp DESC LIMIT 10",
            (student_id,)
        ) as cursor:
            practice = await cursor.fetchall()
        
        # Get quiz results
        async with db.execute(
            "SELECT subject, topic, score, total_questions, timestamp FROM quiz_history WHERE student_id = ? ORDER BY timestamp DESC LIMIT 10",
            (student_id,)
        ) as cursor:
            quizzes = await cursor.fetchall()
        
        return {
            "explained_topics": [
                {"subject": row[0], "topic": row[1], "timestamp": row[2]}
                for row in explained
            ],
            "practice_problems": [
                {"subject": row[0], "topic": row[1], "timestamp": row[2]}
                for row in practice
            ],
            "quiz_results": [
                {
                    "subject": row[0],
                    "topic": row[1],
                    "score": row[2],
                    "total": row[3],
                    "percentage": round((row[2] / row[3]) * 100, 1),
                    "timestamp": row[4]
                }
                for row in quizzes
            ]
        }
