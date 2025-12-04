"""
TrainBot Core Tools
Shared AI logic for educational content generation
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# ============================================
# 🤖 MULTI-PROVIDER AI INTEGRATION
# ============================================

def generate_with_openai(prompt: str) -> str:
    """Generate content using OpenAI API"""
    try:
        import openai
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return "❌ Error: OPENAI_API_KEY not found in environment"
        
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    
    except ImportError:
        return "❌ Error: openai package not installed"
    except Exception as e:
        return f"❌ OpenAI API Error: {str(e)}"


def generate_with_anthropic(prompt: str) -> str:
    """Generate content using Anthropic Claude API"""
    try:
        import anthropic
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return "❌ Error: ANTHROPIC_API_KEY not found in environment"
        
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    
    except ImportError:
        return "❌ Error: anthropic package not installed"
    except Exception as e:
        return f"❌ Anthropic API Error: {str(e)}"


def generate_with_gemini(prompt: str) -> str:
    """Generate content using Google Gemini API"""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return "❌ Error: GEMINI_API_KEY not found in environment"
        
        genai.configure(api_key=api_key)
        
        # Model selection with fallback
        available = [m.name for m in genai.list_models() 
                    if 'generateContent' in m.supported_generation_methods]
        
        priority = [
            "models/gemini-2.0-flash-exp",
            "models/gemini-1.5-pro",
            "models/gemini-1.5-flash"
        ]
        
        model_name = None
        for model in priority:
            if model in available:
                model_name = model
                break
        
        if model_name is None:
            model_name = "models/gemini-1.5-flash"
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    
    except ImportError:
        return "❌ Error: google-generativeai package not installed"
    except Exception as e:
        error_msg = str(e).lower()
        if "quota" in error_msg or "rate" in error_msg:
            return "⚠️ Gemini rate limit reached. Try OpenAI or Anthropic provider."
        return f"❌ Gemini API Error: {str(e)}"


def generate_content(prompt: str, provider: str = "openai") -> str:
    """Universal content generator"""
    provider = provider.lower().strip()
    
    if provider == "openai":
        return generate_with_openai(prompt)
    elif provider in ["anthropic", "claude"]:
        return generate_with_anthropic(prompt)
    elif provider in ["gemini", "google"]:
        return generate_with_gemini(prompt)
    else:
        return f"❌ Unsupported provider: {provider}\n\nUse: openai, anthropic, or gemini"


# ============================================
# 🛠️ EDUCATIONAL TOOLS
# ============================================

def generate_flashcards(topic: str, count: int, level: str, ai_provider: str) -> str:
    """Generate educational flashcards"""
    
    # Validation
    if not topic.strip():
        return "❌ Error: Topic cannot be empty"
    if count < 1 or count > 50:
        return "❌ Error: Count must be between 1 and 50"
    if level.lower() not in ["beginner", "intermediate", "advanced"]:
        return "❌ Error: Level must be beginner, intermediate, or advanced"
    
    prompt = f"""Create exactly {count} educational flashcards on "{topic}".

Level: {level}

Format each flashcard as:
**Card X:**
**Question:** [Question here]
**Answer:** [Answer here]

Make them {level.lower()} level, testing understanding of key concepts with practical applications."""

    return generate_content(prompt, ai_provider)


def generate_course(title: str, modules: int, level: str, duration: str, ai_provider: str) -> str:
    """Generate comprehensive training course"""
    
    # Validation
    if not title.strip():
        return "❌ Error: Title cannot be empty"
    if modules < 1 or modules > 15:
        return "❌ Error: Modules must be between 1 and 15"
    if level.lower() not in ["beginner", "intermediate", "advanced"]:
        return "❌ Error: Level must be beginner, intermediate, or advanced"
    
    prompt = f"""Create a {modules}-module training course on "{title}".

Level: {level}
Duration: {duration}

For each module include:
1. Module title and overview
2. Learning objectives (3-5 objectives)
3. Key concepts with clear explanations
4. Practical examples and use cases
5. Activities or exercises
6. Assessment questions (3-5 questions)

Structure professionally with clear progression."""

    return generate_content(prompt, ai_provider)


def create_quiz(topic: str, questions: int, difficulty: str, include_answers: bool, ai_provider: str) -> str:
    """Create assessment quiz"""
    
    # Validation
    if not topic.strip():
        return "❌ Error: Topic cannot be empty"
    if questions < 1 or questions > 30:
        return "❌ Error: Questions must be between 1 and 30"
    if difficulty.lower() not in ["easy", "medium", "hard", "mixed"]:
        return "❌ Error: Difficulty must be easy, medium, hard, or mixed"
    
    prompt = f"""Create a {questions}-question quiz on "{topic}".

Difficulty: {difficulty}

Include:
- Multiple choice questions (4 options)
- True/False questions
- Short answer questions

Format clearly with question numbers."""

    if include_answers:
        prompt += "\n\nInclude **Answer Key** with correct answers and brief explanations."
    
    return generate_content(prompt, ai_provider)


def explain_topic(topic: str, depth: str, use_analogies: bool, ai_provider: str) -> str:
    """Generate detailed topic explanation"""
    
    # Validation
    if not topic.strip():
        return "❌ Error: Topic cannot be empty"
    if depth.lower() not in ["brief", "comprehensive", "detailed"]:
        return "❌ Error: Depth must be brief, comprehensive, or detailed"
    
    prompt = f"""Explain "{topic}" clearly and educationally.

Depth: {depth}

Include:
- Clear definition and core concepts
- Why this topic is important
- Key principles"""

    if use_analogies:
        prompt += "\n- Relatable analogies and real-world examples"
    
    if depth == "detailed":
        prompt += "\n- Detailed theory\n- Practical applications\n- Common misconceptions"
    
    return generate_content(prompt, ai_provider)


def summarize_content(content: str, summary_type: str, max_length: str, ai_provider: str) -> str:
    """Summarize educational content"""
    
    # Validation
    if not content.strip():
        return "❌ Error: Content cannot be empty"
    if summary_type.lower() not in ["executive", "detailed", "bullet_points"]:
        return "❌ Error: Summary type must be executive, detailed, or bullet_points"
    if max_length.lower() not in ["short", "medium", "long"]:
        return "❌ Error: Length must be short, medium, or long"
    
    # Truncate if too long
    if len(content) > 15000:
        content = content[:15000] + "\n[Content truncated...]"
    
    prompt = f"""Create a {summary_type} summary ({max_length} length).

Content:
{content}

"""

    if summary_type == "executive":
        prompt += "Focus on main insights, key findings, actionable takeaways."
    elif summary_type == "detailed":
        prompt += "Include all major points and supporting information."
    elif summary_type == "bullet_points":
        prompt += "Format as clear, concise bullet points."
    
    return generate_content(prompt, ai_provider)


def create_practice_problems(topic: str, count: int, difficulty: str, include_solutions: bool, ai_provider: str) -> str:
    """Generate practice problems"""
    
    # Validation
    if not topic.strip():
        return "❌ Error: Topic cannot be empty"
    if count < 1 or count > 20:
        return "❌ Error: Count must be between 1 and 20"
    if difficulty.lower() not in ["easy", "medium", "hard", "progressive"]:
        return "❌ Error: Difficulty must be easy, medium, hard, or progressive"
    
    prompt = f"""Create {count} practice problems on "{topic}".

Difficulty: {difficulty}

For each problem:
1. State clearly with context
2. Make practical and realistic"""

    if difficulty == "progressive":
        prompt += "\n\nStart easy and gradually increase difficulty."
    
    if include_solutions:
        prompt += "\n\nInclude **Solutions** section with:\n- Step-by-step approach\n- Key concepts\n- Final answer"
    
    return generate_content(prompt, ai_provider)