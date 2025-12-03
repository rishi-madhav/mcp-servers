"""
StudyBuddy - AI Learning Companion
Final deployment version with dark theme and formatted output
"""

import gradio as gr
import json
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server import database as db
from mcp_server.openai_client import get_openai_client
from mcp_server import prompts

# Global state
current_student_id = None
current_grade = 8
current_board = "CBSE"
current_topic = ""
current_subject = ""

# Subject mappings
SUBJECTS_BY_GRADE = {
    5: ["Mathematics", "Science", "English", "Social Studies", "Hindi"],
    6: ["Mathematics", "Science", "English", "Social Studies", "Hindi"],
    7: ["Mathematics", "Science", "English", "Social Studies", "Hindi"],
    8: ["Mathematics", "Science", "English", "Social Studies", "Hindi", "Computer Science"],
    9: ["Mathematics", "Science", "English", "Social Studies", "Hindi", "Computer Science"],
    10: ["Mathematics", "Science", "English", "Social Studies", "Hindi", "Computer Science"]
}

def get_subjects_for_grade(grade):
    """Update subject dropdown based on grade."""
    grade_num = int(grade.replace("Grade ", ""))
    return gr.update(choices=SUBJECTS_BY_GRADE.get(grade_num, []), value=None)

def initialize_student(name: str, grade: str, board: str):
    """Initialize student profile."""
    global current_student_id, current_grade, current_board
    
    if not name:
        return "⚠️ Please enter your name"
    
    async def _init():
        global current_student_id, current_grade, current_board
        await db.init_database()
        grade_num = int(grade.replace("Grade ", ""))
        current_student_id = await db.get_or_create_student(name, grade_num, board)
        current_grade = grade_num
        current_board = board
        return f"✅ Welcome {name}! ({grade}, {board})"
    
    return asyncio.run(_init())

def set_topic_subject(topic: str, subject: str):
    """Set current topic and subject."""
    global current_topic, current_subject
    if not topic or not subject:
        return "⚠️ Please select both topic and subject"
    current_topic = topic
    current_subject = subject
    return f"📚 **{topic}** in {subject}"

# Formatting functions for human-readable output
def format_explanation(result):
    if "error" in result:
        return f"❌ **Error:** {result.get('suggestion', result['error'])}"
    
    output = f"# {result.get('topic', 'Explanation')}\n\n"
    output += f"{result.get('explanation', '')}\n\n"
    output += "## 💡 Key Points\n\n"
    for point in result.get('key_points', []):
        output += f"- {point}\n"
    output += f"\n## 🌍 Real-World Example\n\n{result.get('real_world_example', '')}"
    return output

def format_practice(result):
    if "error" in result:
        return f"❌ **Error:** {result.get('suggestion', result['error'])}"
    
    output = f"# Practice Problems: {result.get('topic', '')}\n\n"
    for i, p in enumerate(result.get('problems', []), 1):
        output += f"## Problem {i} ({p.get('difficulty', 'medium').title()})\n\n"
        output += f"**Question:** {p.get('question', '')}\n\n"
        output += f"**💡 Hint:** {p.get('hint', '')}\n\n"
        output += f"**✓ Answer:** {p.get('answer', '')}\n\n"
        output += f"**Explanation:** {p.get('explanation', '')}\n\n---\n\n"
    return output

def format_solution(result):
    if "error" in result:
        return f"❌ **Error:** {result.get('suggestion', result['error'])}"
    
    output = f"# Step-by-Step Solution\n\n**Problem:** {result.get('problem', '')}\n\n"
    for step in result.get('steps', []):
        output += f"## Step {step.get('step_number', '')}: {step.get('description', '')}\n\n"
        output += f"```\n{step.get('work', '')}\n```\n\n"
        output += f"💡 {step.get('explanation', '')}\n\n"
    output += f"## ✅ Final Answer\n\n**{result.get('final_answer', '')}**"
    return output

def format_story(result):
    if "error" in result:
        return f"❌ **Error:** {result.get('suggestion', result['error'])}"
    
    output = f"# {result.get('story_title', 'Story')}\n\n"
    output += f"{result.get('story', '')}\n\n"
    output += f"**Characters:** {', '.join(result.get('characters', []))}\n\n"
    output += "**What You Learned:**\n"
    for concept in result.get('key_concepts_taught', []):
        output += f"- {concept}\n"
    return output

def format_quiz(result):
    if "error" in result:
        return f"❌ **Error:** {result.get('suggestion', result['error'])}"
    
    output = f"# Quiz: {result.get('topic', '')}\n\n"
    for i, q in enumerate(result.get('questions', [])[:10], 1):
        output += f"## Question {i} ({q.get('difficulty', 'medium').title()})\n\n"
        output += f"{q.get('question', '')}\n\n"
        if q.get('type') in ['mcq', 'true_false']:
            output += "**Options:**\n"
            for opt in q.get('options', []):
                output += f"- {opt}\n"
        output += f"\n**✓ Answer:** {q.get('correct_answer', '')}\n\n---\n\n"
    return output

def format_progress(history):
    output = "# 📊 Your Learning Progress\n\n"
    output += f"- **Topics Explained:** {len(history.get('explained_topics', []))}\n"
    output += f"- **Practice Sessions:** {len(history.get('practice_problems', []))}\n"
    output += f"- **Quizzes Taken:** {len(history.get('quiz_results', []))}\n\n"
    output += "## Recent Activity\n\n"
    for topic in history.get('explained_topics', [])[:5]:
        output += f"- 📖 {topic['topic']} ({topic['subject']})\n"
    return output

# Tool functions
def explain_topic():
    if not current_student_id or not current_topic:
        return "⚠️ Please complete setup and select a topic"
    
    async def _explain():
        openai = get_openai_client()
        prompt = prompts.get_explain_prompt(current_topic, current_grade, current_board, current_subject)
        result = await openai.generate_content(prompt)
        if "error" not in result:
            await db.save_explanation(current_student_id, current_subject, current_topic, result.get("explanation", ""))
        return format_explanation(result)
    
    return asyncio.run(_explain())

def generate_practice(num: int):
    if not current_student_id or not current_topic:
        return "⚠️ Please complete setup and select a topic"
    
    async def _gen():
        openai = get_openai_client()
        prompt = prompts.get_practice_prompt(current_topic, current_grade, current_board, current_subject, num)
        result = await openai.generate_content(prompt)
        if "error" not in result:
            await db.save_practice_problems(current_student_id, current_subject, current_topic, result.get("problems", []))
        return format_practice(result)
    
    return asyncio.run(_gen())

def solve_problem(problem: str):
    if not problem:
        return "⚠️ Please enter a problem"
    
    async def _solve():
        openai = get_openai_client()
        prompt = prompts.get_solve_step_by_step_prompt(problem, current_subject or "Mathematics", current_grade)
        result = await openai.generate_content(prompt)
        return format_solution(result)
    
    return asyncio.run(_solve())

def create_story():
    if not current_topic:
        return "⚠️ Please select a topic"
    
    async def _story():
        openai = get_openai_client()
        prompt = prompts.get_story_prompt(current_topic, current_grade, current_subject)
        result = await openai.generate_content(prompt)
        return format_story(result)
    
    return asyncio.run(_story())

def quiz_me():
    if not current_student_id or not current_topic:
        return "⚠️ Please complete setup and select a topic"
    
    async def _quiz():
        previous = await db.get_quiz_history(current_student_id, current_subject, current_topic)
        openai = get_openai_client()
        prompt = prompts.get_quiz_prompt(current_topic, current_grade, current_board, current_subject, previous)
        result = await openai.generate_content(prompt)
        return format_quiz(result)
    
    return asyncio.run(_quiz())

def get_progress():
    if not current_student_id:
        return "⚠️ Please set up profile"
    
    async def _hist():
        history = await db.get_student_history(current_student_id)
        return format_progress(history)
    
    return asyncio.run(_hist())

# Dark Theme CSS
css = """
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

body, .gradio-container {
    font-family: 'Montserrat', sans-serif !important;
    background: #1D1821 !important;
    color: #E5E5E5 !important;
}

.sidebar {
    background: #27222E;
    border-right: 1px solid #3A3540;
    padding: 2rem 1.5rem;
}

.sidebar-logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: #9A76D9;
    margin-bottom: 2rem;
}

label { color: #E5E5E5 !important; font-weight: 600 !important; }

input, select, textarea {
    background: #27222E !important;
    border: 1.5px solid #3A3540 !important;
    color: #E5E5E5 !important;
    border-radius: 8px !important;
    padding: 0.75rem !important;
}

input:focus, select:focus, textarea:focus {
    border-color: #9A76D9 !important;
    box-shadow: 0 0 0 3px rgba(154, 118, 217, 0.2) !important;
}

button[variant="primary"] {
    background: linear-gradient(135deg, #9A76D9, #B794F6) !important;
    color: white !important;
    border: none !important;
    padding: 0.875rem 1.5rem !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

.gr-tabs {
    background: #27222E !important;
    border: 1px solid #3A3540 !important;
    padding: 1.5rem !important;
    border-radius: 12px !important;
}

.gr-button {
    color: #9A9A9A !important;
    background: transparent !important;
}

.gr-button.selected {
    color: #9A76D9 !important;
    border-bottom: 3px solid #9A76D9 !important;
}

.gr-markdown {
    background: #27222E !important;
    border: 1px solid #3A3540 !important;
    padding: 1.5rem !important;
    border-radius: 12px !important;
    color: #E5E5E5 !important;
}

.gr-markdown h1 { color: #9A76D9 !important; }
.gr-markdown h2 { color: #9A76D9 !important; }
.gr-panel { background: #27222E !important; }
"""

# Build UI
with gr.Blocks(css=css, theme=gr.themes.Soft(), title="StudyBuddy") as demo:
    with gr.Row():
        # Sidebar
        with gr.Column(scale=0, min_width=320, elem_classes="sidebar"):
            gr.HTML('<div class="sidebar-logo">🎓 StudyBuddy</div>')
            
            gr.Markdown("### 👤 Student Profile")
            student_name = gr.Textbox(label="Name", placeholder="Enter your name", value="")
            student_grade = gr.Dropdown(label="Grade", choices=["Grade 5", "Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10"], value="Grade 8")
            student_board = gr.Dropdown(label="Board", choices=["CBSE", "ICSE", "IGCSE"], value="CBSE")
            profile_btn = gr.Button("Create Profile", variant="primary")
            profile_status = gr.Markdown("*Not set*")
            
            gr.Markdown("### 📚 Select Topic")
            subject_dropdown = gr.Dropdown(label="Subject", choices=SUBJECTS_BY_GRADE[8])
            topic_input = gr.Textbox(label="Topic", placeholder="e.g., Decimals", value="")
            topic_btn = gr.Button("Set Topic", variant="primary")
            topic_status = gr.Markdown("*Not set*")
        
        # Canvas
        with gr.Column(scale=1):
            gr.Markdown("# Learning Tools")
            gr.Markdown("Choose a tool below to start learning")
            
            with gr.Tabs():
                with gr.Tab("📖 Learn"):
                    learn_btn = gr.Button("✨ Explain Topic", variant="primary", size="lg")
                    learn_output = gr.Markdown()
                
                with gr.Tab("✏️ Practice"):
                    practice_num = gr.Slider(label="Problems", minimum=1, maximum=10, value=5)
                    practice_btn = gr.Button("📝 Generate", variant="primary", size="lg")
                    practice_output = gr.Markdown()
                
                with gr.Tab("🔍 Solve"):
                    problem_input = gr.Textbox(label="Problem", placeholder="e.g., Solve: 2x + 5 = 15", lines=3)
                    solve_btn = gr.Button("🧮 Solve", variant="primary", size="lg")
                    solve_output = gr.Markdown()
                
                with gr.Tab("📖 Story"):
                    story_btn = gr.Button("🎨 Create Story", variant="primary", size="lg")
                    story_output = gr.Markdown()
                
                with gr.Tab("🎯 Quiz"):
                    quiz_btn = gr.Button("🎲 Start Quiz", variant="primary", size="lg")
                    quiz_output = gr.Markdown()
                
                with gr.Tab("📊 Progress"):
                    progress_btn = gr.Button("📈 View Progress", variant="primary", size="lg")
                    progress_output = gr.Markdown()
            
            gr.Markdown("---")
            gr.Markdown("*Powered by OpenAI GPT-4o-mini • Built with MCP & Gradio*")
    
    # Events
    student_grade.change(fn=get_subjects_for_grade, inputs=[student_grade], outputs=[subject_dropdown])
    profile_btn.click(fn=initialize_student, inputs=[student_name, student_grade, student_board], outputs=[profile_status])
    topic_btn.click(fn=set_topic_subject, inputs=[topic_input, subject_dropdown], outputs=[topic_status])
    
    learn_btn.click(fn=explain_topic, outputs=[learn_output])
    practice_btn.click(fn=generate_practice, inputs=[practice_num], outputs=[practice_output])
    solve_btn.click(fn=solve_problem, inputs=[problem_input], outputs=[solve_output])
    story_btn.click(fn=create_story, outputs=[story_output])
    quiz_btn.click(fn=quiz_me, outputs=[quiz_output])
    progress_btn.click(fn=get_progress, outputs=[progress_output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861, share=False)
