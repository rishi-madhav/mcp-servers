"""Structured prompts for MCP tools that Claude will use via Gemini API."""

def get_explain_prompt(topic: str, grade: int, board: str, subject: str) -> str:
    """Generate prompt for explaining a topic."""
    return f"""You are a certified school teacher creating safe, educational content for children.

STUDENT CONTEXT: Grade {grade} student (age 10-15), studying {subject} in {board} curriculum
TOPIC: {topic}
PURPOSE: Help student understand this standard school mathematics/science concept

Please provide a simple, safe, child-appropriate explanation that includes:
- What this concept means in simple terms
- A real-world example students can relate to  
- Three key learning points

Keep language positive, educational, and suitable for young learners.

Return valid JSON:
{{
    "topic": "{topic}",
    "grade": {grade},
    "explanation": "Child-friendly explanation here",
    "key_points": ["Point 1", "Point 2", "Point 3"],
    "real_world_example": "Safe, relatable example"
}}"""

def get_practice_prompt(topic: str, grade: int, board: str, subject: str, num_questions: int = 5) -> str:
    """Generate prompt for practice problems."""
    return f"""You are creating practice problems for a grade {grade} {board} student studying {subject}.

Topic: "{topic}"

Generate {num_questions} practice problems that:
1. Match {board} exam patterns
2. Progress from easy to challenging
3. Include variety (MCQ, short answer, numerical)
4. Are grade {grade} appropriate

CRITICAL: Respond with ONLY valid JSON. No markdown, no code blocks, no extra text.
Make sure all quotes inside strings are properly escaped.

{{
    "topic": "{topic}",
    "problems": [
        {{
            "question": "problem statement here",
            "type": "mcq",
            "difficulty": "easy",
            "hint": "optional hint",
            "answer": "correct answer",
            "explanation": "solution explanation"
        }}
    ]
}}"""

def get_solve_step_by_step_prompt(problem: str, subject: str, grade: int) -> str:
    """Generate prompt for step-by-step problem solving."""
    return f"""You are a {subject} tutor helping a grade {grade} student solve this problem:

"{problem}"

Provide a complete step-by-step solution that:
1. Identifies what is given and what needs to be found
2. Shows each calculation or reasoning step clearly
3. Explains WHY each step is taken
4. Highlights key formulas or concepts used
5. Verifies the final answer

CRITICAL: Respond with ONLY valid JSON. No markdown, no code blocks, no extra text.

{{
    "problem": "{problem}",
    "steps": [
        {{
            "step_number": 1,
            "description": "what we are doing in this step",
            "work": "calculations or reasoning",
            "explanation": "why this step is necessary"
        }}
    ],
    "final_answer": "the answer with units if applicable",
    "key_concepts": ["concept 1", "concept 2"]
}}"""

def get_story_prompt(topic: str, grade: int, subject: str) -> str:
    """Generate prompt for turning topics into engaging stories."""
    return f"""You are creating a safe, educational story for grade {grade} students learning about {topic} in {subject} class.

Create a SHORT educational story (under 250 words) with:
- Friendly characters appropriate for children
- Simple language teaching about {topic}
- A positive, educational message
- No quotes inside the story text (use apostrophes only)

Return valid JSON with story on a single line:
{{
    "topic": "{topic}",
    "story_title": "Fun title here",
    "story": "Once upon a time there was a friendly character who learned about {topic}. The story continues here teaching the concept in a fun way and ends happily.",
    "characters": ["Character 1", "Character 2"],
    "key_concepts_taught": ["Concept 1", "Concept 2"],
    "discussion_questions": ["Question 1", "Question 2"]
}}"""

def get_quiz_prompt(
    topic: str, 
    grade: int, 
    board: str, 
    subject: str, 
    previous_questions: list
) -> str:
    """Generate prompt for quiz questions, avoiding previous questions."""
    prev_q_text = ""
    if previous_questions:
        prev_q_text = "\n\nIMPORTANT: Do NOT repeat these previously asked questions:\n" + "\n".join(
            f"- {q}" for q in previous_questions[-20:]  # Last 20 questions
        )
    
    return f"""You are creating a quiz for a grade {grade} {board} student on {subject}.

Topic: "{topic}"

Generate exactly 10 quiz questions that:
1. Match {board} exam style
2. Mix difficulty levels (3 easy, 4 medium, 3 hard)
3. Include variety (MCQ, true/false, short answer)
4. Test conceptual understanding, not just memorization
5. Are appropriate for grade {grade}{prev_q_text}

CRITICAL: Respond with ONLY valid JSON. Generate exactly 10 questions.

{{
    "topic": "{topic}",
    "questions": [
        {{
            "question_number": 1,
            "question": "the question text",
            "type": "mcq",
            "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
            "correct_answer": "the correct answer",
            "explanation": "why this is correct",
            "difficulty": "easy"
        }}
    ]
}}

For true/false questions, use type: "true_false" and options: ["True", "False"]
For short answer, use type: "short_answer" and options: []

Generate exactly 10 questions."""
