"""
TrainBot - AI-Powered Educational Content Generator
Premium Professional Interface for Gradio
"""

import gradio as gr
from trainbot_tools import (
    generate_flashcards,
    generate_course,
    create_quiz,
    explain_topic,
    summarize_content,
    create_practice_problems
)

# ============================================
# 🎨 PREMIUM PROFESSIONAL DESIGN
# ============================================

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=JetBrains+Mono:wght@300;500;700&family=Inter:wght@300;400;600;800&display=swap');

:root {
    --obsidian: #1a1a2e;
    --slate: #16213e;
    --pearl: #f8f9fa;
    --gold: #d4a574;
    --copper: #c17c5a;
    --sage: #95a792;
    --charcoal: #2d2d3a;
    --mist: #e8eaed;
    --shadow-soft: rgba(0, 0, 0, 0.08);
    --shadow-strong: rgba(0, 0, 0, 0.16);
}

body {
    background: linear-gradient(135deg, #f8f9fa 0%, #e8eaed 100%);
    background-attachment: fixed;
}

.gradio-container {
    max-width: 1600px !important;
    margin: auto;
    font-family: 'Inter', sans-serif !important;
    color: var(--obsidian) !important;
}

/* Elegant Masthead */
.masthead {
    background: linear-gradient(135deg, var(--obsidian) 0%, var(--slate) 100%);
    padding: 60px 48px;
    margin-bottom: 48px;
    border-radius: 12px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px var(--shadow-strong);
}

.masthead::before {
    content: "";
    position: absolute;
    top: -50%;
    right: -10%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(212, 165, 116, 0.15), transparent 70%);
    animation: float 20s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    50% { transform: translate(-30px, 30px) rotate(10deg); }
}

.masthead h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 72px !important;
    font-weight: 900 !important;
    color: var(--pearl) !important;
    letter-spacing: -1px;
    margin: 0 0 16px 0 !important;
    line-height: 1.1 !important;
    position: relative;
    z-index: 2;
}

.masthead .tagline {
    font-family: 'Inter', sans-serif !important;
    font-size: 18px !important;
    font-weight: 300 !important;
    color: var(--mist) !important;
    margin: 16px 0 !important;
    letter-spacing: 0.5px;
    position: relative;
    z-index: 2;
}

.masthead .providers {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--gold) !important;
    margin-top: 24px !important;
    letter-spacing: 1px;
    position: relative;
    z-index: 2;
}

/* Provider Selection Panel */
.provider-panel {
    background: white;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 32px;
    box-shadow: 0 2px 8px var(--shadow-soft);
}

/* Refined Tabs */
.tabs {
    border-bottom: 2px solid var(--mist);
    margin-bottom: 32px;
}

button[role="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    color: var(--charcoal) !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    padding: 16px 28px !important;
    margin: 0 4px !important;
    transition: all 0.3s ease;
    letter-spacing: 0.3px;
}

button[role="tab"]:hover {
    color: var(--copper) !important;
    background: rgba(193, 124, 90, 0.05) !important;
}

button[role="tab"][aria-selected="true"] {
    color: var(--copper) !important;
    border-bottom-color: var(--copper) !important;
    background: rgba(193, 124, 90, 0.08) !important;
}

/* Input Controls */
.input-panel {
    background: white;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 8px;
    padding: 28px;
    box-shadow: 0 2px 8px var(--shadow-soft);
}

textarea, input[type="text"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    color: var(--obsidian) !important;
    background: var(--pearl) !important;
    border: 1px solid rgba(0, 0, 0, 0.12) !important;
    border-radius: 6px !important;
    padding: 12px 16px !important;
    transition: all 0.3s ease;
    line-height: 1.6 !important;
}

textarea:focus, input[type="text"]:focus {
    border-color: var(--copper) !important;
    box-shadow: 0 0 0 3px rgba(193, 124, 90, 0.1) !important;
    outline: none !important;
    background: white !important;
}

/* Labels */
label {
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: var(--charcoal) !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px !important;
    display: block;
}

/* Buttons */
button.primary {
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    color: white !important;
    background: linear-gradient(135deg, var(--copper) 0%, var(--gold) 100%) !important;
    border: none !important;
    padding: 14px 32px !important;
    border-radius: 6px !important;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(193, 124, 90, 0.3);
    text-transform: uppercase;
}

button.primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(193, 124, 90, 0.4);
}

button.primary:active {
    transform: translateY(0);
}

/* Dropdown */
select {
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    color: var(--obsidian) !important;
    background: white !important;
    border: 1px solid rgba(0, 0, 0, 0.12) !important;
    padding: 12px 16px !important;
    border-radius: 6px !important;
    cursor: pointer;
    transition: all 0.3s ease;
}

select:hover {
    border-color: var(--copper);
    box-shadow: 0 2px 8px var(--shadow-soft);
}

select:focus {
    border-color: var(--copper);
    box-shadow: 0 0 0 3px rgba(193, 124, 90, 0.1);
    outline: none;
}

/* Sliders */
input[type="range"] {
    -webkit-appearance: none;
    background: linear-gradient(to right, var(--copper), var(--gold)) !important;
    height: 6px;
    border-radius: 3px;
}

input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 20px;
    height: 20px;
    background: white;
    border: 3px solid var(--copper);
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 2px 8px var(--shadow-soft);
    transition: all 0.2s ease;
}

input[type="range"]::-webkit-slider-thumb:hover {
    transform: scale(1.1);
    border-color: var(--gold);
}

/* Radio & Checkbox */
input[type="radio"], input[type="checkbox"] {
    accent-color: var(--copper) !important;
    transform: scale(1.15);
    cursor: pointer;
}

/* Output Display */
.output-display {
    background: var(--pearl) !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    border-radius: 8px !important;
    padding: 24px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
    color: var(--obsidian) !important;
    box-shadow: inset 0 1px 3px var(--shadow-soft);
    min-height: 500px !important;
}

/* Section Headers */
.section-header {
    font-family: 'Playfair Display', serif !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    color: var(--obsidian) !important;
    margin-bottom: 24px !important;
    padding-bottom: 12px !important;
    border-bottom: 2px solid var(--mist);
}

/* Footer */
.footer-info {
    margin-top: 64px;
    padding: 40px;
    background: white;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 8px;
    box-shadow: 0 2px 8px var(--shadow-soft);
}

.footer-info h3 {
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    color: var(--copper) !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 16px !important;
}

.footer-info p, .footer-info li {
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    color: var(--charcoal) !important;
    line-height: 1.7 !important;
}

.footer-info a {
    color: var(--copper) !important;
    text-decoration: none !important;
    font-weight: 600 !important;
    border-bottom: 1px solid transparent;
    transition: all 0.2s ease;
}

.footer-info a:hover {
    border-bottom-color: var(--copper);
}

.footer-info code {
    font-family: 'JetBrains Mono', monospace !important;
    background: var(--mist);
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 13px;
    color: var(--copper);
    border: 1px solid rgba(0, 0, 0, 0.08);
}

/* Staggered Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.gradio-container > div {
    animation: fadeIn 0.6s ease-out both;
}

.provider-panel {
    animation-delay: 0.1s;
}

.tabs {
    animation-delay: 0.2s;
}

/* Responsive */
@media (max-width: 768px) {
    .masthead h1 {
        font-size: 42px !important;
    }
    
    .masthead {
        padding: 40px 24px;
    }
}
"""

with gr.Blocks(css=custom_css, title="TrainBot — AI Educational Content Generator", theme=gr.themes.Base()) as demo:
    
    # Professional Masthead
    gr.HTML("""
    <div class="masthead">
        <h1>TrainBot</h1>
        <p class="tagline">AI-powered educational content generation with enterprise-grade flexibility</p>
        <p class="providers">Multi-Provider Support: OpenAI • Anthropic • Google Gemini</p>
    </div>
    """)
    
    # Provider Selection
    with gr.Row(elem_classes=["provider-panel"]):
        with gr.Column(scale=1):
            ai_provider_global = gr.Dropdown(
                choices=["openai", "anthropic", "gemini"],
                value="openai",
                label="AI Provider",
                info="Select your preferred model provider",
                interactive=True
            )
    
    # Main Tabs
    with gr.Tabs(elem_classes=["tabs"]) as tabs:
        
        # 1. Content Summarizer
        with gr.Tab("Content Summarizer"):
            gr.Markdown('<div class="section-header">Summarize Educational Content</div>')
            with gr.Row():
                with gr.Column(scale=1, elem_classes=["input-panel"]):
                    summarize_content_input = gr.Textbox(
                        label="Content",
                        placeholder="Paste your content here...",
                        lines=10
                    )
                    summarize_type = gr.Radio(
                        choices=["executive", "detailed", "bullet_points"],
                        value="executive",
                        label="Summary Type"
                    )
                    summarize_length = gr.Radio(
                        choices=["short", "medium", "long"],
                        value="medium",
                        label="Length"
                    )
                    summarize_generate_btn = gr.Button("Generate Summary", variant="primary")
                
                with gr.Column(scale=2):
                    summarize_output = gr.Textbox(
                        label="Generated Summary",
                        lines=22,
                        show_copy_button=True,
                        elem_classes=["output-display"]
                    )
            
            summarize_generate_btn.click(
                fn=summarize_content,
                inputs=[summarize_content_input, summarize_type, summarize_length, ai_provider_global],
                outputs=summarize_output
            )
        
        # 2. Course Builder
        with gr.Tab("Course Builder"):
            gr.Markdown('<div class="section-header">Create Comprehensive Training Course</div>')
            with gr.Row():
                with gr.Column(scale=1, elem_classes=["input-panel"]):
                    course_title = gr.Textbox(
                        label="Course Title",
                        placeholder="e.g., Introduction to Data Science",
                        lines=2
                    )
                    course_modules = gr.Slider(
                        minimum=1,
                        maximum=15,
                        value=5,
                        step=1,
                        label="Number of Modules"
                    )
                    course_level = gr.Radio(
                        choices=["beginner", "intermediate", "advanced"],
                        value="intermediate",
                        label="Difficulty Level"
                    )
                    course_duration = gr.Textbox(
                        label="Duration",
                        value="1 week",
                        placeholder="e.g., 1 week, 3 days, 2 months"
                    )
                    course_generate_btn = gr.Button("Generate Course", variant="primary")
                
                with gr.Column(scale=2):
                    course_output = gr.Textbox(
                        label="Generated Course",
                        lines=22,
                        show_copy_button=True,
                        elem_classes=["output-display"]
                    )
            
            course_generate_btn.click(
                fn=generate_course,
                inputs=[course_title, course_modules, course_level, course_duration, ai_provider_global],
                outputs=course_output
            )
        
        # 3. Topic Explainer
        with gr.Tab("Topic Explainer"):
            gr.Markdown('<div class="section-header">Generate Topic Explanation</div>')
            with gr.Row():
                with gr.Column(scale=1, elem_classes=["input-panel"]):
                    explain_topic_input = gr.Textbox(
                        label="Topic",
                        placeholder="e.g., Recursion, Photosynthesis, Blockchain",
                        lines=2
                    )
                    explain_depth = gr.Radio(
                        choices=["brief", "comprehensive", "detailed"],
                        value="comprehensive",
                        label="Explanation Depth"
                    )
                    explain_analogies = gr.Checkbox(
                        label="Include Analogies & Examples",
                        value=True
                    )
                    explain_generate_btn = gr.Button("Generate Explanation", variant="primary")
                
                with gr.Column(scale=2):
                    explain_output = gr.Textbox(
                        label="Generated Explanation",
                        lines=22,
                        show_copy_button=True,
                        elem_classes=["output-display"]
                    )
            
            explain_generate_btn.click(
                fn=explain_topic,
                inputs=[explain_topic_input, explain_depth, explain_analogies, ai_provider_global],
                outputs=explain_output
            )
        
        # 4. Quiz Creator
        with gr.Tab("Quiz Creator"):
            gr.Markdown('<div class="section-header">Create Assessment Quiz</div>')
            with gr.Row():
                with gr.Column(scale=1, elem_classes=["input-panel"]):
                    quiz_topic = gr.Textbox(
                        label="Quiz Topic",
                        placeholder="e.g., Python Data Structures, European History",
                        lines=2
                    )
                    quiz_questions = gr.Slider(
                        minimum=1,
                        maximum=30,
                        value=10,
                        step=1,
                        label="Number of Questions"
                    )
                    quiz_difficulty = gr.Radio(
                        choices=["easy", "medium", "hard", "mixed"],
                        value="mixed",
                        label="Difficulty"
                    )
                    quiz_answers = gr.Checkbox(
                        label="Include Answer Key",
                        value=True
                    )
                    quiz_generate_btn = gr.Button("Create Quiz", variant="primary")
                
                with gr.Column(scale=2):
                    quiz_output = gr.Textbox(
                        label="Generated Quiz",
                        lines=22,
                        show_copy_button=True,
                        elem_classes=["output-display"]
                    )
            
            quiz_generate_btn.click(
                fn=create_quiz,
                inputs=[quiz_topic, quiz_questions, quiz_difficulty, quiz_answers, ai_provider_global],
                outputs=quiz_output
            )
        
        # 5. Practice Problems
        with gr.Tab("Practice Problems"):
            gr.Markdown('<div class="section-header">Generate Practice Problems</div>')
            with gr.Row():
                with gr.Column(scale=1, elem_classes=["input-panel"]):
                    practice_topic = gr.Textbox(
                        label="Topic",
                        placeholder="e.g., Python Loops, Calculus, SQL Queries",
                        lines=2
                    )
                    practice_count = gr.Slider(
                        minimum=1,
                        maximum=20,
                        value=5,
                        step=1,
                        label="Number of Problems"
                    )
                    practice_difficulty = gr.Radio(
                        choices=["easy", "medium", "hard", "progressive"],
                        value="progressive",
                        label="Difficulty"
                    )
                    practice_solutions = gr.Checkbox(
                        label="Include Solutions",
                        value=True
                    )
                    practice_generate_btn = gr.Button("Generate Problems", variant="primary")
                
                with gr.Column(scale=2):
                    practice_output = gr.Textbox(
                        label="Generated Problems",
                        lines=22,
                        show_copy_button=True,
                        elem_classes=["output-display"]
                    )
            
            practice_generate_btn.click(
                fn=create_practice_problems,
                inputs=[practice_topic, practice_count, practice_difficulty, practice_solutions, ai_provider_global],
                outputs=practice_output
            )
        
        # 6. Flashcards Generator
        with gr.Tab("Flashcards Generator"):
            gr.Markdown('<div class="section-header">Generate Educational Flashcards</div>')
            with gr.Row():
                with gr.Column(scale=1, elem_classes=["input-panel"]):
                    fc_topic = gr.Textbox(
                        label="Topic",
                        placeholder="e.g., Machine Learning Fundamentals, World War II Timeline",
                        lines=2
                    )
                    fc_count = gr.Slider(
                        minimum=1,
                        maximum=50,
                        value=10,
                        step=1,
                        label="Number of Cards"
                    )
                    fc_level = gr.Radio(
                        choices=["beginner", "intermediate", "advanced"],
                        value="intermediate",
                        label="Difficulty Level"
                    )
                    fc_generate_btn = gr.Button("Generate Flashcards", variant="primary")
                
                with gr.Column(scale=2):
                    fc_output = gr.Textbox(
                        label="Generated Flashcards",
                        lines=22,
                        show_copy_button=True,
                        elem_classes=["output-display"]
                    )
            
            fc_generate_btn.click(
                fn=generate_flashcards,
                inputs=[fc_topic, fc_count, fc_level, ai_provider_global],
                outputs=fc_output
            )
    
    # Footer Documentation
    gr.HTML("""
    <div class="footer-info">
        <h3>Setup Instructions</h3>
        <p>To use TrainBot on HuggingFace Spaces, configure your API keys as Secrets in your Space settings:</p>
        <ul style="list-style-type: '—'; padding-left: 24px; margin-top: 16px;">
            <li><code>OPENAI_API_KEY</code> — Required for OpenAI GPT models</li>
            <li><code>ANTHROPIC_API_KEY</code> — Optional for Anthropic Claude models</li>
            <li><code>GEMINI_API_KEY</code> — Optional for Google Gemini models</li>
        </ul>
        
        <h3 style="margin-top: 32px;">About TrainBot</h3>
        <p>
            TrainBot is a multi-provider AI content generation platform designed for educators, 
            trainers, content creators, and students. Generate comprehensive educational materials 
            including courses, quizzes, flashcards, explanations, summaries, and practice problems 
            using your choice of leading AI providers.
        </p>
        <p style="margin-top: 20px;">
            <a href="https://github.com/rishi-madhav/mcp-servers" target="_blank">View on GitHub</a> • 
            Built by Rishi Madhav • Bengaluru, India
        </p>
    </div>
    """)

# Launch
if __name__ == "__main__":
    demo.launch()