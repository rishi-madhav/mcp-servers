"""Structured prompts for MCP tools that Claude will use to generate educational content."""

def get_explain_prompt(topic: str, grade: int, board: str, subject: str) -> str:
    """Generate prompt for explaining a topic."""
    return f"""You are an expert {board} {subject} tutor for grade {grade} students.

Explain the topic: "{topic}"

Requirements:
1. Use age-appropriate language for grade {grade}
2. Align with {board} curriculum standards
3. Include:
   - Simple definition
   - Real-world examples
   - Key concepts to remember
   - Common misconceptions to avoid
4. Keep explanation between 200-400 words
5. Use analogies that resonate with {grade}th graders

CRITICAL: Respond with ONLY valid JSON. No markdown, no code blocks, no extra text.
Make sure all quotes inside strings are properly escaped.

{{
    "topic": "{topic}",
    "grade": {grade},
    "explanation": "your detailed explanation here (escape any quotes inside)",
    "key_points": ["point 1", "point 2", "point 3"],
    "real_world_example": "example description"
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

Respond ONLY with a JSON object in this exact format:
{{
    "problem": "{problem}",
    "steps": [
        {{
            "step_number": 1,
            "description": "what we're doing in this step",
            "work": "calculations or reasoning",
            "explanation": "why this step is necessary"
        }}
    ],
    "final_answer": "the answer with units if applicable",
    "key_concepts": ["concept 1", "concept 2"]
}}

DO NOT include any text outside the JSON structure."""

def get_story_prompt(topic: str, grade: int, subject: str) -> str:
    """Generate prompt for turning topics into engaging stories."""
    return f"""You are a creative educator transforming dry {subject} topics into engaging stories for grade {grade} students.

Topic: "{topic}"

Create an engaging story that:
1. Features relatable characters (kids, animals, or fantasy characters)
2. Naturally incorporates the key concepts of {topic}
3. Has a clear beginning, middle, and end
4. Makes learning fun and memorable
5. Is appropriate for grade {grade} reading level
6. Length: 200-400 words (keep it concise to avoid JSON errors)

CRITICAL JSON FORMATTING:
- Use ONLY plain quotes in the JSON structure
- NEVER use quotes inside the story text - use apostrophes instead
- Keep the story concise (under 400 words)
- No line breaks or special characters in strings

Example of correct format:
{{
    "topic": "Water Cycle",
    "story_title": "Droplet's Amazing Journey",
    "story": "Once upon a time, a water droplet named Dewey lived in the ocean. One sunny day, the sun's warmth lifted Dewey up into the sky through evaporation. He joined millions of other droplets to form a fluffy cloud...",
    "characters": ["Dewey the droplet", "Sunny the sun"],
    "key_concepts_taught": ["Evaporation", "Condensation"],
    "discussion_questions": ["What made Dewey rise into the sky?"]
}}

Now create the story for "{topic}":

def get_quiz_prompt(
    topic: str, 
    grade: int, 
    board: str, 
    subject: str, 
    previous_questions: list[str]
) -> str:
    """Generate prompt for quiz questions, avoiding previous questions."""
    prev_q_text = ""
    if previous_questions:
        prev_q_text = f"\n\nIMPORTANT: Do NOT repeat these previously asked questions:\n" + "\n".join(
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

Respond ONLY with a JSON object in this exact format:
{{
    "topic": "{topic}",
    "questions": [
        {{
            "question_number": 1,
            "question": "the question text",
            "type": "mcq|true_false|short_answer",
            "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
            "correct_answer": "the correct answer",
            "explanation": "why this is correct",
            "difficulty": "easy|medium|hard"
        }}
    ]
}}

For true/false questions, use options: ["True", "False"]
For short answer, use options: []

DO NOT include any text outside the JSON structure. Generate exactly 10 questions."""
