"""StudyBuddy MCP Server - Educational tools for Indian students (Grades 5-10)."""

import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field

from . import database as db
from . import prompts

# Initialize MCP server
app = Server("studybuddy")

# Student context (single student per session)
class StudentContext(BaseModel):
    name: str = Field(default="Student", description="Student name")
    grade: int = Field(default=8, ge=5, le=10, description="Grade level (5-10)")
    board: str = Field(default="CBSE", description="Education board (CBSE/ICSE/IGCSE)")
    student_id: int | None = Field(default=None, description="Database student ID")

# Global student context (persists during session)
_student_context = StudentContext()

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available educational tools."""
    return [
        Tool(
            name="studybuddy_explain_topic",
            description="Explain any topic at grade-appropriate level aligned with CBSE/ICSE/IGCSE curriculum. Returns structured explanation with key points and examples.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to explain (e.g., 'Photosynthesis', 'Quadratic Equations')"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Subject name (e.g., 'Science', 'Mathematics', 'English')"
                    },
                    "grade": {
                        "type": "integer",
                        "description": "Grade level (5-10)",
                        "minimum": 5,
                        "maximum": 10
                    },
                    "board": {
                        "type": "string",
                        "description": "Education board",
                        "enum": ["CBSE", "ICSE", "IGCSE"]
                    }
                },
                "required": ["topic", "subject", "grade", "board"]
            },
            annotations={
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True
            }
        ),
        Tool(
            name="studybuddy_generate_practice",
            description="Generate practice questions for any topic with varying difficulty levels and question types (MCQ, short answer, numerical).",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic for practice problems"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Subject name"
                    },
                    "grade": {
                        "type": "integer",
                        "description": "Grade level (5-10)",
                        "minimum": 5,
                        "maximum": 10
                    },
                    "board": {
                        "type": "string",
                        "description": "Education board",
                        "enum": ["CBSE", "ICSE", "IGCSE"]
                    },
                    "num_questions": {
                        "type": "integer",
                        "description": "Number of practice problems to generate (default: 5)",
                        "minimum": 1,
                        "maximum": 10,
                        "default": 5
                    }
                },
                "required": ["topic", "subject", "grade", "board"]
            },
            annotations={
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": False
            }
        ),
        Tool(
            name="studybuddy_solve_step_by_step",
            description="Solve math/science problems with detailed step-by-step explanations, showing all work and reasoning.",
            inputSchema={
                "type": "object",
                "properties": {
                    "problem": {
                        "type": "string",
                        "description": "The complete problem statement to solve"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Subject (typically 'Mathematics' or 'Science')"
                    },
                    "grade": {
                        "type": "integer",
                        "description": "Grade level (5-10)",
                        "minimum": 5,
                        "maximum": 10
                    }
                },
                "required": ["problem", "subject", "grade"]
            },
            annotations={
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True
            }
        ),
        Tool(
            name="studybuddy_create_story",
            description="Turn boring topics into fun, engaging stories with relatable characters. Makes learning memorable and enjoyable.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to convert into a story"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Subject name"
                    },
                    "grade": {
                        "type": "integer",
                        "description": "Grade level (5-10)",
                        "minimum": 5,
                        "maximum": 10
                    }
                },
                "required": ["topic", "subject", "grade"]
            },
            annotations={
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": False
            }
        ),
        Tool(
            name="studybuddy_quiz_me",
            description="Generate a 10-question quiz on any topic. Tracks previously asked questions to avoid repeats. Returns questions with answers and explanations for self-assessment.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to quiz on"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Subject name"
                    },
                    "grade": {
                        "type": "integer",
                        "description": "Grade level (5-10)",
                        "minimum": 5,
                        "maximum": 10
                    },
                    "board": {
                        "type": "string",
                        "description": "Education board",
                        "enum": ["CBSE", "ICSE", "IGCSE"]
                    }
                },
                "required": ["topic", "subject", "grade", "board"]
            },
            annotations={
                "readOnlyHint": False,
                "destructiveHint": False,
                "idempotentHint": False
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    
    # Ensure database is initialized
    await db.init_database()
    
    # Get or create student ID
    if _student_context.student_id is None:
        grade = arguments.get("grade", _student_context.grade)
        board = arguments.get("board", _student_context.board)
        _student_context.student_id = await db.get_or_create_student(
            _student_context.name, 
            grade, 
            board
        )
    
    try:
        if name == "studybuddy_explain_topic":
            return await handle_explain_topic(arguments)
        
        elif name == "studybuddy_generate_practice":
            return await handle_generate_practice(arguments)
        
        elif name == "studybuddy_solve_step_by_step":
            return await handle_solve_step_by_step(arguments)
        
        elif name == "studybuddy_create_story":
            return await handle_create_story(arguments)
        
        elif name == "studybuddy_quiz_me":
            return await handle_quiz_me(arguments)
        
        else:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": f"Unknown tool: {name}",
                    "available_tools": [
                        "studybuddy_explain_topic",
                        "studybuddy_generate_practice",
                        "studybuddy_solve_step_by_step",
                        "studybuddy_create_story",
                        "studybuddy_quiz_me"
                    ]
                })
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": str(e),
                "tool": name,
                "suggestion": "Check that all required parameters are provided with correct types."
            })
        )]

async def handle_explain_topic(args: dict) -> list[TextContent]:
    """Handle explain_topic tool call with Gemini API."""
    from .gemini_client import get_gemini_client
    
    topic = args["topic"]
    subject = args["subject"]
    grade = args["grade"]
    board = args["board"]
    
    # Generate prompt
    prompt = prompts.get_explain_prompt(topic, grade, board, subject)
    
    # Call Gemini API
    gemini = get_gemini_client()
    result = await gemini.generate_content(prompt)
    
    # Save to database if successful
    if "error" not in result and _student_context.student_id:
        explanation_text = result.get("explanation", "")
        if explanation_text:
            await db.save_explanation(
                _student_context.student_id,
                subject,
                topic,
                explanation_text
            )
    
    # Add metadata
    result["metadata"] = {
        "tool": "explain_topic",
        "topic": topic,
        "subject": subject,
        "grade": grade,
        "board": board,
        "powered_by": "Google Gemini 2.5 Flash"
    }
    
    return [TextContent(type="text", text=json.dumps(result, indent=2))]

async def handle_generate_practice(args: dict) -> list[TextContent]:
    """Handle generate_practice tool call with Gemini API."""
    from .gemini_client import get_gemini_client
    
    topic = args["topic"]
    subject = args["subject"]
    grade = args["grade"]
    board = args["board"]
    num_questions = args.get("num_questions", 5)
    
    # Generate prompt
    prompt = prompts.get_practice_prompt(topic, grade, board, subject, num_questions)
    
    # Call Gemini API
    gemini = get_gemini_client()
    result = await gemini.generate_content(prompt)
    
    # Save to database if successful
    if "error" not in result and _student_context.student_id:
        problems = result.get("problems", [])
        if problems:
            await db.save_practice_problems(
                _student_context.student_id,
                subject,
                topic,
                problems
            )
    
    # Add metadata
    result["metadata"] = {
        "tool": "generate_practice",
        "topic": topic,
        "subject": subject,
        "grade": grade,
        "board": board,
        "num_questions": num_questions,
        "powered_by": "Google Gemini 2.5 Flash"
    }
    
    return [TextContent(type="text", text=json.dumps(result, indent=2))]

async def handle_solve_step_by_step(args: dict) -> list[TextContent]:
    """Handle solve_step_by_step tool call with Gemini API."""
    from .gemini_client import get_gemini_client
    
    problem = args["problem"]
    subject = args["subject"]
    grade = args["grade"]
    
    # Generate prompt
    prompt = prompts.get_solve_step_by_step_prompt(problem, subject, grade)
    
    # Call Gemini API
    gemini = get_gemini_client()
    result = await gemini.generate_content(prompt)
    
    # Add metadata
    result["metadata"] = {
        "tool": "solve_step_by_step",
        "problem": problem,
        "subject": subject,
        "grade": grade,
        "powered_by": "Google Gemini 2.5 Flash"
    }
    
    return [TextContent(type="text", text=json.dumps(result, indent=2))]

async def handle_create_story(args: dict) -> list[TextContent]:
    """Handle create_story tool call with Gemini API."""
    from .gemini_client import get_gemini_client
    
    topic = args["topic"]
    subject = args["subject"]
    grade = args["grade"]
    
    # Generate prompt
    prompt = prompts.get_story_prompt(topic, grade, subject)
    
    # Call Gemini API
    gemini = get_gemini_client()
    result = await gemini.generate_content(prompt)
    
    # Add metadata
    result["metadata"] = {
        "tool": "create_story",
        "topic": topic,
        "subject": subject,
        "grade": grade,
        "powered_by": "Google Gemini 2.5 Flash"
    }
    
    return [TextContent(type="text", text=json.dumps(result, indent=2))]

async def handle_quiz_me(args: dict) -> list[TextContent]:
    """Handle quiz_me tool call with Gemini API and duplicate avoidance."""
    from .gemini_client import get_gemini_client
    
    topic = args["topic"]
    subject = args["subject"]
    grade = args["grade"]
    board = args["board"]
    
    # Get previously asked questions
    previous_questions = await db.get_quiz_history(
        _student_context.student_id,
        subject,
        topic
    )
    
    # Generate prompt with previous questions
    prompt = prompts.get_quiz_prompt(topic, grade, board, subject, previous_questions)
    
    # Call Gemini API
    gemini = get_gemini_client()
    result = await gemini.generate_content(prompt)
    
    # Save to database if successful (without score initially)
    if "error" not in result and _student_context.student_id:
        questions = result.get("questions", [])
        if questions:
            # Save with score=0 initially (will be updated when user completes quiz)
            await db.save_quiz_result(
                _student_context.student_id,
                subject,
                topic,
                questions,
                score=0  # Updated later by Gradio app
            )
    
    # Add metadata
    result["metadata"] = {
        "tool": "quiz_me",
        "topic": topic,
        "subject": subject,
        "grade": grade,
        "board": board,
        "total_questions": 10,
        "previous_questions_avoided": len(previous_questions),
        "powered_by": "Google Gemini 2.5 Flash"
    }
    
    return [TextContent(type="text", text=json.dumps(result, indent=2))]

async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
