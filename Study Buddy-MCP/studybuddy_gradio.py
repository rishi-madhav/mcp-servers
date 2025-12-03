"""
StudyBuddy Web Interface - Enhanced Educational Assistant
Gradio interface for the StudyBuddy MCP server functionality
"""

import gradio as gr
import json
import sqlite3
import os
import asyncio
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Import our MCP server functions
import sys
sys.path.append('.')

# We'll import the core functions from the MCP server
from studybuddy_mcp_server import (
    call_gemini, validate_json_response, get_user_id, log_activity,
    get_previous_quiz_questions, store_quiz_questions,
    get_explain_prompt, get_practice_prompt, get_solve_prompt,
    get_story_prompt, get_quiz_prompt, init_database
)

load_dotenv()

# Ensure database is initialized
init_database()

# Custom CSS for StudyBuddy theme
custom_css = """
/* StudyBuddy Theme */
.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.studybuddy-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    text-align: center;
}

.profile-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}

.feature-card {
    background: white;
    border: 2px solid #e1e5e9;
    border-radius: 12px;
    padding: 20px;
    margin: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.feature-card:hover {
    border-color: #667eea;
    box-shadow: 0 8px 15px rgba(102, 126, 234, 0.2);
}

.success-message {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    padding: 12px;
    border-radius: 6px;
    margin: 10px 0;
}

.error-message {
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
    padding: 12px;
    border-radius: 6px;
    margin: 10px 0;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin: 20px 0;
}

.stat-card {
    background: white;
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.json-output {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    padding: 15px;
    font-family: 'Monaco', 'Courier New', monospace;
    font-size: 12px;
    max-height: 400px;
    overflow-y: auto;
    white-space: pre-wrap;
}

.footer {display: none !important;}
"""

# Global state
current_user = {"name": "", "grade": 0, "board": ""}

# ============================================
# CORE FUNCTIONS
# ============================================

def setup_profile(name, grade, board):
    """Setup user profile"""
    global current_user
    
    if not name or not grade or not board:
        return "❌ Please fill in all profile fields", "", "Please complete your profile setup"
    
    if grade < 5 or grade > 10:
        return "❌ Grade must be between 5 and 10", "", "Invalid grade selected"
    
    current_user = {"name": name, "grade": grade, "board": board}
    
    # Create/update user in database
    user_id = get_user_id(name, grade, board)
    
    welcome_msg = f"✅ Welcome, {name}! (Grade {grade}, {board})"
    profile_display = f"**Student:** {name} | **Grade:** {grade} | **Board:** {board}"
    
    return welcome_msg, profile_display, "Profile setup complete! You can now use all StudyBuddy tools."

def explain_topic_interface(topic, subject):
    """Interface for topic explanation"""
    if not current_user["name"]:
        return "❌ Please setup your profile first!"
    
    if not topic or not subject:
        return "❌ Please enter both topic and subject"
    
    try:
        # Get user ID
        user_id = get_user_id(current_user["name"], current_user["grade"], current_user["board"])
        
        # Generate explanation
        prompt = get_explain_prompt(topic, subject, current_user["grade"], current_user["board"])
        response = call_gemini(prompt)
        result = validate_json_response(response)
        
        # Log activity
        log_activity(user_id, "explanation", topic, subject, result)
        
        # Format for display
        explanation = result.get("explanation", "No explanation available")
        key_points = result.get("key_points", [])
        real_world_example = result.get("real_world_example", "")
        fun_fact = result.get("fun_fact", "")
        
        formatted_output = f"""
## 📚 {topic} ({subject})

### Explanation:
{explanation}

### Key Points:
{chr(10).join([f"• {point}" for point in key_points])}

### Real-World Example:
{real_world_example}

### Fun Fact:
{fun_fact}

---
*Generated for {current_user['name']} (Grade {current_user['grade']}, {current_user['board']})*
        """
        
        return formatted_output
        
    except Exception as e:
        return f"❌ Error explaining topic: {str(e)}"

def generate_practice_interface(topic, subject, num_questions):
    """Interface for practice problem generation"""
    if not current_user["name"]:
        return "❌ Please setup your profile first!"
    
    if not topic or not subject:
        return "❌ Please enter both topic and subject"
    
    try:
        # Get user ID
        user_id = get_user_id(current_user["name"], current_user["grade"], current_user["board"])
        
        # Generate practice problems
        prompt = get_practice_prompt(topic, subject, current_user["grade"], current_user["board"], num_questions)
        response = call_gemini(prompt)
        result = validate_json_response(response)
        
        # Log activity
        log_activity(user_id, "practice_problems", topic, subject, result)
        
        # Format for display
        problems = result.get("problems", [])
        
        formatted_output = f"""
## ✏️ Practice Problems: {topic} ({subject})

"""
        
        for i, problem in enumerate(problems, 1):
            formatted_output += f"""
### Problem {i} ({problem.get('difficulty', 'medium').title()})
**Question:** {problem.get('question', 'No question')}

**Solution:**
{problem.get('solution', 'No solution available')}

**Answer:** {problem.get('answer', 'No answer')}

---
"""
        
        formatted_output += f"\n*Generated {len(problems)} problems for {current_user['name']} (Grade {current_user['grade']}, {current_user['board']})*"
        
        return formatted_output
        
    except Exception as e:
        return f"❌ Error generating practice problems: {str(e)}"

def solve_problem_interface(problem, subject):
    """Interface for step-by-step problem solving"""
    if not current_user["name"]:
        return "❌ Please setup your profile first!"
    
    if not problem or not subject:
        return "❌ Please enter both problem and subject"
    
    try:
        # Get user ID
        user_id = get_user_id(current_user["name"], current_user["grade"], "GENERAL")
        
        # Generate solution
        prompt = get_solve_prompt(problem, subject, current_user["grade"])
        response = call_gemini(prompt)
        result = validate_json_response(response)
        
        # Log activity
        log_activity(user_id, "problem_solved", f"Problem: {problem[:50]}...", subject, result)
        
        # Format for display
        problem_type = result.get("problem_type", "Unknown")
        given_info = result.get("given_information", [])
        steps = result.get("steps", [])
        final_answer = result.get("final_answer", "No answer")
        verification = result.get("verification", "")
        
        formatted_output = f"""
## 🔍 Step-by-Step Solution

### Problem:
{problem}

### Problem Type:
{problem_type}

### Given Information:
{chr(10).join([f"• {info}" for info in given_info])}

### Solution Steps:
"""
        
        for step in steps:
            formatted_output += f"""
**Step {step.get('step_number', '?')}:** {step.get('description', 'No description')}

{step.get('work', 'No work shown')}

*Result:* {step.get('result', 'No result')}

"""
        
        formatted_output += f"""
### Final Answer:
**{final_answer}**

### Verification:
{verification}

---
*Solved for {current_user['name']} (Grade {current_user['grade']})*
        """
        
        return formatted_output
        
    except Exception as e:
        return f"❌ Error solving problem: {str(e)}"

def create_story_interface(topic, subject):
    """Interface for story creation"""
    if not current_user["name"]:
        return "❌ Please setup your profile first!"
    
    if not topic or not subject:
        return "❌ Please enter both topic and subject"
    
    try:
        # Get user ID
        user_id = get_user_id(current_user["name"], current_user["grade"], "GENERAL")
        
        # Generate story
        prompt = get_story_prompt(topic, subject, current_user["grade"])
        response = call_gemini(prompt)
        result = validate_json_response(response)
        
        # Log activity
        log_activity(user_id, "story_created", topic, subject, result)
        
        # Format for display
        story_title = result.get("story_title", "Educational Story")
        story = result.get("story", "No story available")
        characters = result.get("main_characters", [])
        concepts = result.get("key_concepts_taught", [])
        questions = result.get("discussion_questions", [])
        
        formatted_output = f"""
# 📖 {story_title}

## The Story:
{story}

## Characters:
{chr(10).join([f"• {char}" for char in characters])}

## Key Concepts Taught:
{chr(10).join([f"• {concept}" for concept in concepts])}

## Discussion Questions:
{chr(10).join([f"{i+1}. {q}" for i, q in enumerate(questions)])}

---
*Story created for {current_user['name']} (Grade {current_user['grade']})*
        """
        
        return formatted_output
        
    except Exception as e:
        return f"❌ Error creating story: {str(e)}"

def quiz_interface(topic, subject):
    """Interface for quiz generation"""
    if not current_user["name"]:
        return "❌ Please setup your profile first!"
    
    if not topic or not subject:
        return "❌ Please enter both topic and subject"
    
    try:
        # Get user ID
        user_id = get_user_id(current_user["name"], current_user["grade"], current_user["board"])
        
        # Get previous questions to avoid duplicates
        previous_questions = get_previous_quiz_questions(user_id, topic)
        
        # Generate quiz
        prompt = get_quiz_prompt(topic, subject, current_user["grade"], current_user["board"], previous_questions)
        response = call_gemini(prompt)
        result = validate_json_response(response)
        
        # Store new questions
        if "questions" in result:
            new_questions = [q["question"] for q in result["questions"]]
            store_quiz_questions(user_id, topic, new_questions)
        
        # Log activity
        log_activity(user_id, "quiz_completed", topic, subject, result)
        
        # Format for display
        questions = result.get("questions", [])
        
        formatted_output = f"""
# 🎯 Quiz: {topic} ({subject})

*Estimated Time: {result.get('estimated_time', '15-20 minutes')}*
*Questions avoided from previous attempts: {len(previous_questions)}*

"""
        
        for i, q in enumerate(questions, 1):
            question_text = q.get("question", "No question")
            q_type = q.get("type", "unknown")
            options = q.get("options", [])
            correct_answer = q.get("correct_answer", "No answer")
            explanation = q.get("explanation", "No explanation")
            difficulty = q.get("difficulty", "medium")
            
            formatted_output += f"""
## Question {i} ({difficulty.title()})
**{question_text}**

"""
            
            if options:
                for option in options:
                    formatted_output += f"{option}\n"
            
            formatted_output += f"""
<details>
<summary><strong>Click for Answer & Explanation</strong></summary>

**Answer:** {correct_answer}

**Explanation:** {explanation}
</details>

---

"""
        
        formatted_output += f"\n*Quiz generated for {current_user['name']} with {len(questions)} unique questions*"
        
        return formatted_output
        
    except Exception as e:
        return f"❌ Error generating quiz: {str(e)}"

def get_progress_interface():
    """Interface for progress tracking"""
    if not current_user["name"]:
        return "❌ Please setup your profile first!"
    
    try:
        conn = sqlite3.connect("studybuddy_data.db")
        cursor = conn.cursor()
        
        # Get user profiles
        cursor.execute(
            "SELECT id, grade, board, created_at FROM user_profiles WHERE name = ? ORDER BY last_active DESC",
            (current_user["name"],)
        )
        profiles = cursor.fetchall()
        
        if not profiles:
            return "📊 No learning history found yet. Start using StudyBuddy tools to build your progress!"
        
        formatted_output = f"# 📊 Learning Progress: {current_user['name']}\n\n"
        
        for profile_id, grade, board, created_at in profiles:
            # Get activity counts
            cursor.execute(
                "SELECT activity_type, COUNT(*) FROM learning_activities WHERE user_id = ? GROUP BY activity_type",
                (profile_id,)
            )
            activity_counts = dict(cursor.fetchall())
            
            # Get recent activities
            cursor.execute(
                "SELECT activity_type, topic, subject, created_at FROM learning_activities WHERE user_id = ? ORDER BY created_at DESC LIMIT 5",
                (profile_id,)
            )
            recent_activities = cursor.fetchall()
            
            total_activities = sum(activity_counts.values())
            
            formatted_output += f"""
## Profile: Grade {grade}, {board}
*Started: {created_at}*

### Activity Summary:
• **Total Activities:** {total_activities}
• **Topics Explained:** {activity_counts.get('explanation', 0)}
• **Practice Problems:** {activity_counts.get('practice_problems', 0)}
• **Problems Solved:** {activity_counts.get('problem_solved', 0)}
• **Stories Created:** {activity_counts.get('story_created', 0)}
• **Quizzes Completed:** {activity_counts.get('quiz_completed', 0)}

### Recent Activities:
"""
            
            for activity_type, topic, subject, activity_date in recent_activities:
                formatted_output += f"• **{activity_type.replace('_', ' ').title()}:** {topic} ({subject}) - {activity_date[:10]}\n"
            
            formatted_output += "\n---\n"
        
        conn.close()
        return formatted_output
        
    except Exception as e:
        return f"❌ Error retrieving progress: {str(e)}"

# ============================================
# GRADIO INTERFACE
# ============================================

def create_studybuddy_interface():
    """Create the main StudyBuddy Gradio interface"""
    
    with gr.Blocks(css=custom_css, title="StudyBuddy - AI Learning Assistant") as app:
        
        # Header
        gr.Markdown("""
        <div class="studybuddy-header">
            <h1>🎓 StudyBuddy - Your AI Learning Assistant</h1>
            <p>Personalized learning for Indian students (Grades 5-10) | CBSE • ICSE • IGCSE</p>
        </div>
        """)
        
        # Profile Setup
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 👤 Student Profile")
                name_input = gr.Textbox(
                    label="Your Name",
                    placeholder="Enter your name",
                    info="This helps us personalize your learning experience"
                )
                grade_input = gr.Slider(
                    minimum=5, maximum=10, step=1, value=8,
                    label="Grade",
                    info="Your current grade (5-10)"
                )
                board_input = gr.Dropdown(
                    choices=["CBSE", "ICSE", "IGCSE"],
                    value="CBSE",
                    label="Education Board",
                    info="Your curriculum board"
                )
                setup_btn = gr.Button("Setup Profile", variant="primary")
                
            with gr.Column(scale=1):
                profile_status = gr.Markdown("Please setup your profile to get started")
                profile_display = gr.Markdown("")
        
        setup_status = gr.Markdown("")
        
        # Main Tools Interface
        with gr.Tabs():
            
            # Explain Topic
            with gr.Tab("📚 Explain Topic"):
                gr.Markdown("""
                ### Get Grade-Appropriate Explanations
                Ask for clear explanations of any topic aligned with your curriculum.
                """)
                
                with gr.Row():
                    explain_topic = gr.Textbox(
                        label="Topic to Explain",
                        placeholder="e.g., Photosynthesis, Quadratic Equations, World War 1",
                        scale=2
                    )
                    explain_subject = gr.Textbox(
                        label="Subject",
                        placeholder="e.g., Science, Mathematics, History",
                        scale=1
                    )
                
                explain_btn = gr.Button("🔍 Explain Topic", variant="primary")
                explain_output = gr.Markdown("")
            
            # Practice Problems
            with gr.Tab("✏️ Practice Problems"):
                gr.Markdown("""
                ### Generate Custom Practice Problems
                Get practice questions with step-by-step solutions for any topic.
                """)
                
                with gr.Row():
                    practice_topic = gr.Textbox(
                        label="Topic",
                        placeholder="e.g., Fractions, Cell Division, Grammar",
                        scale=2
                    )
                    practice_subject = gr.Textbox(
                        label="Subject",
                        placeholder="e.g., Mathematics, Biology, English",
                        scale=1
                    )
                    practice_num = gr.Slider(
                        minimum=1, maximum=10, step=1, value=5,
                        label="Number of Problems"
                    )
                
                practice_btn = gr.Button("📝 Generate Problems", variant="primary")
                practice_output = gr.Markdown("")
            
            # Solve Problem
            with gr.Tab("🔍 Solve Problem"):
                gr.Markdown("""
                ### Step-by-Step Problem Solving
                Get detailed solutions with explanations for any math or science problem.
                """)
                
                with gr.Row():
                    solve_problem = gr.Textbox(
                        label="Problem Statement",
                        placeholder="e.g., Solve: 2x + 5 = 15",
                        lines=3,
                        scale=2
                    )
                    solve_subject = gr.Textbox(
                        label="Subject",
                        placeholder="e.g., Mathematics, Physics, Chemistry",
                        scale=1
                    )
                
                solve_btn = gr.Button("🧮 Solve Step-by-Step", variant="primary")
                solve_output = gr.Markdown("")
            
            # Story Mode
            with gr.Tab("📖 Story Mode"):
                gr.Markdown("""
                ### Turn Topics into Engaging Stories
                Make learning fun with stories that teach concepts naturally.
                """)
                
                with gr.Row():
                    story_topic = gr.Textbox(
                        label="Topic to Story-fy",
                        placeholder="e.g., Water Cycle, Gravity, Friendship",
                        scale=2
                    )
                    story_subject = gr.Textbox(
                        label="Subject",
                        placeholder="e.g., Science, Physics, Life Skills",
                        scale=1
                    )
                
                story_btn = gr.Button("📚 Create Story", variant="primary")
                story_output = gr.Markdown("")
            
            # Quiz Me
            with gr.Tab("🎯 Quiz Me"):
                gr.Markdown("""
                ### Test Your Knowledge
                Get personalized quizzes that avoid repeating previous questions.
                """)
                
                with gr.Row():
                    quiz_topic = gr.Textbox(
                        label="Quiz Topic",
                        placeholder="e.g., Digestive System, Indian History, Algebra",
                        scale=2
                    )
                    quiz_subject = gr.Textbox(
                        label="Subject",
                        placeholder="e.g., Biology, Social Studies, Mathematics",
                        scale=1
                    )
                
                quiz_btn = gr.Button("🎲 Start Quiz", variant="primary")
                quiz_output = gr.Markdown("")
            
            # My Progress
            with gr.Tab("📊 My Progress"):
                gr.Markdown("""
                ### Track Your Learning Journey
                See your learning statistics and recent activities.
                """)
                
                progress_btn = gr.Button("📈 Load My Progress", variant="primary")
                progress_output = gr.Markdown("")
        
        # Footer
        gr.Markdown("""
        ---
        <div style="text-align: center; color: #666; margin-top: 20px;">
            <p><strong>StudyBuddy</strong> - Making learning personalized and fun for every student</p>
            <p>Built with ❤️ for Indian students | Powered by AI</p>
        </div>
        """)
        
        # ============================================
        # EVENT HANDLERS
        # ============================================
        
        # Profile setup
        setup_btn.click(
            setup_profile,
            inputs=[name_input, grade_input, board_input],
            outputs=[setup_status, profile_display, profile_status]
        )
        
        # Tool interactions
        explain_btn.click(
            explain_topic_interface,
            inputs=[explain_topic, explain_subject],
            outputs=[explain_output]
        )
        
        practice_btn.click(
            generate_practice_interface,
            inputs=[practice_topic, practice_subject, practice_num],
            outputs=[practice_output]
        )
        
        solve_btn.click(
            solve_problem_interface,
            inputs=[solve_problem, solve_subject],
            outputs=[solve_output]
        )
        
        story_btn.click(
            create_story_interface,
            inputs=[story_topic, story_subject],
            outputs=[story_output]
        )
        
        quiz_btn.click(
            quiz_interface,
            inputs=[quiz_topic, quiz_subject],
            outputs=[quiz_output]
        )
        
        progress_btn.click(
            get_progress_interface,
            outputs=[progress_output]
        )
    
    return app

# ============================================
# LAUNCH
# ============================================

if __name__ == "__main__":
    # Verify environment
    if not os.getenv('GEMINI_API_KEY'):
        print("⚠️  WARNING: GEMINI_API_KEY not found in environment variables")
        print("Please add your Gemini API key to continue.")
        exit(1)
    
    print("🎓 Starting StudyBuddy Web Interface...")
    print("📊 Database initialized")
    print("🚀 Ready for learning!")
    
    # Create and launch interface
    app = create_studybuddy_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7861,
        show_error=True,
        share=False
    )
