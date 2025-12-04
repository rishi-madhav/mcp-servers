"""
TrainBot MCP Server - Multi-Provider Edition
An AI-powered training course generation tool built with FastMCP.

Supports multiple AI providers: OpenAI, Anthropic (Claude), and Google Gemini
"""

import os
from typing import Optional
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the FastMCP server
mcp = FastMCP("TrainBot")

# ============================================
# 🤖 MULTI-PROVIDER AI INTEGRATION
# ============================================

def generate_with_openai(prompt: str) -> str:
    """Generate content using OpenAI API"""
    try:
        import openai
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return "Error: OPENAI_API_KEY not found in .env file"
        
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    
    except ImportError:
        return "Error: openai package not installed. Run: pip install openai"
    except Exception as e:
        return f"OpenAI API Error: {str(e)}"


def generate_with_anthropic(prompt: str) -> str:
    """Generate content using Anthropic Claude API"""
    try:
        import anthropic
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return "Error: ANTHROPIC_API_KEY not found in .env file"
        
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    
    except ImportError:
        return "Error: anthropic package not installed. Run: pip install anthropic"
    except Exception as e:
        return f"Anthropic API Error: {str(e)}"


def generate_with_gemini(prompt: str) -> str:
    """Generate content using Google Gemini API"""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return "Error: GEMINI_API_KEY not found in .env file"
        
        genai.configure(api_key=api_key)
        
        # Use priority fallback for model selection
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
        return "Error: google-generativeai package not installed. Run: pip install google-generativeai"
    except Exception as e:
        error_msg = str(e).lower()
        if "quota" in error_msg or "rate" in error_msg:
            return "⚠️ Gemini API rate limit reached. Try 'openai' or 'anthropic' provider, or wait a moment."
        return f"Gemini API Error: {str(e)}"


def generate_content(prompt: str, provider: str = "openai") -> str:
    """
    Universal content generator supporting multiple AI providers.
    
    Parameters:
    -----------
    prompt : str
        The prompt to send to the AI
    provider : str
        AI provider: "openai", "anthropic", or "gemini"
    
    Returns:
    --------
    str
        Generated content from the specified provider
    """
    provider = provider.lower().strip()
    
    if provider == "openai":
        return generate_with_openai(prompt)
    elif provider == "anthropic" or provider == "claude":
        return generate_with_anthropic(prompt)
    elif provider == "gemini" or provider == "google":
        return generate_with_gemini(prompt)
    else:
        return f"❌ Error: Unsupported provider '{provider}'\n\nSupported providers:\n• openai (GPT-4o-mini)\n• anthropic (Claude 3.5 Haiku)\n• gemini (Gemini 2.0 Flash)"


# ============================================
# 🛠️ MCP TOOLS
# ============================================

@mcp.tool()
def generate_flashcards(
    topic: str, 
    count: int = 10, 
    level: str = "intermediate",
    ai_provider: str = "openai"
) -> str:
    """
    Generate educational flashcards for a given topic.

    This tool creates flashcards to help learners study a topic effectively.

    Parameters:
    -----------
    topic : str
        The subject or topic for flashcards.
        Example: "Python programming", "World War II", "Photosynthesis"

    count : int, optional
        Number of flashcards to generate (default: 10, range: 1-50)

    level : str, optional
        Difficulty: "beginner", "intermediate", or "advanced" (default: "intermediate")

    ai_provider : str, optional
        AI provider: "openai", "anthropic", or "gemini" (default: "openai")

    Returns:
    --------
    str
        Formatted flashcards with questions and answers
    """
    # Validate inputs
    if count <= 0 or count > 50:
        return "Error: count must be between 1 and 50"
    
    if level.lower() not in ["beginner", "intermediate", "advanced"]:
        return "Error: level must be 'beginner', 'intermediate', or 'advanced'"
    
    # Generate flashcards
    prompt = f"""Create exactly {count} educational flashcards on "{topic}".

Level: {level}

Format each flashcard as:
**Card X:**
**Question:** [Question here]
**Answer:** [Answer here]

Make them {level.lower()} level, testing understanding of key concepts with practical applications."""

    return generate_content(prompt, ai_provider)


@mcp.tool()
def generate_course(
    title: str, 
    modules: int = 5, 
    level: str = "intermediate",
    duration: str = "1 week",
    ai_provider: str = "openai"
) -> str:
    """
    Generate a comprehensive training course.

    Parameters:
    -----------
    title : str
        Course title/topic

    modules : int, optional
        Number of modules (default: 5, range: 1-15)

    level : str, optional
        Difficulty: "beginner", "intermediate", or "advanced"
    
    duration : str, optional
        Expected duration (default: "1 week")
    
    ai_provider : str, optional
        AI provider: "openai", "anthropic", or "gemini"

    Returns:
    --------
    str
        Complete course with modules, objectives, and assessments
    """
    if modules <= 0 or modules > 15:
        return "Error: modules must be between 1 and 15"
    
    if level.lower() not in ["beginner", "intermediate", "advanced"]:
        return "Error: level must be 'beginner', 'intermediate', or 'advanced'"
    
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


@mcp.tool()
def create_quiz(
    topic: str, 
    questions: int = 10, 
    difficulty: str = "mixed",
    include_answers: bool = True,
    ai_provider: str = "openai"
) -> str:
    """
    Create an assessment quiz.

    Parameters:
    -----------
    topic : str
        Quiz subject

    questions : int, optional
        Number of questions (default: 10, range: 1-30)

    difficulty : str, optional
        Difficulty: "easy", "medium", "hard", or "mixed"
    
    include_answers : bool, optional
        Include answer key (default: True)
    
    ai_provider : str, optional
        AI provider: "openai", "anthropic", or "gemini"

    Returns:
    --------
    str
        Quiz with multiple choice, true/false, and short answer questions
    """
    if questions <= 0 or questions > 30:
        return "Error: questions must be between 1 and 30"
    
    if difficulty.lower() not in ["easy", "medium", "hard", "mixed"]:
        return "Error: difficulty must be 'easy', 'medium', 'hard', or 'mixed'"
    
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


@mcp.tool()
def explain_topic(
    topic: str, 
    depth: str = "comprehensive",
    use_analogies: bool = True,
    ai_provider: str = "openai"
) -> str:
    """
    Generate detailed topic explanation.

    Parameters:
    -----------
    topic : str
        Concept to explain

    depth : str, optional
        Depth: "brief", "comprehensive", or "detailed"

    use_analogies : bool, optional
        Include analogies and examples (default: True)
    
    ai_provider : str, optional
        AI provider: "openai", "anthropic", or "gemini"

    Returns:
    --------
    str
        Well-structured explanation
    """
    if depth.lower() not in ["brief", "comprehensive", "detailed"]:
        return "Error: depth must be 'brief', 'comprehensive', or 'detailed'"
    
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


@mcp.tool()
def summarize_content(
    content: str, 
    summary_type: str = "executive",
    max_length: str = "medium",
    ai_provider: str = "openai"
) -> str:
    """
    Summarize educational content.

    Parameters:
    -----------
    content : str
        Content to summarize

    summary_type : str, optional
        Type: "executive", "detailed", or "bullet_points"

    max_length : str, optional
        Length: "short", "medium", or "long"
    
    ai_provider : str, optional
        AI provider: "openai", "anthropic", or "gemini"

    Returns:
    --------
    str
        Structured summary
    """
    if not content.strip():
        return "Error: content cannot be empty"
    
    if summary_type.lower() not in ["executive", "detailed", "bullet_points"]:
        return "Error: summary_type must be 'executive', 'detailed', or 'bullet_points'"
    
    if max_length.lower() not in ["short", "medium", "long"]:
        return "Error: max_length must be 'short', 'medium', or 'long'"
    
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


@mcp.tool()
def create_practice_problems(
    topic: str, 
    count: int = 5, 
    difficulty: str = "progressive",
    include_solutions: bool = True,
    ai_provider: str = "openai"
) -> str:
    """
    Generate practice problems.

    Parameters:
    -----------
    topic : str
        Subject area

    count : int, optional
        Number of problems (default: 5, range: 1-20)

    difficulty : str, optional
        Difficulty: "easy", "medium", "hard", or "progressive"

    include_solutions : bool, optional
        Include step-by-step solutions (default: True)
    
    ai_provider : str, optional
        AI provider: "openai", "anthropic", or "gemini"

    Returns:
    --------
    str
        Practice problems with optional solutions
    """
    if count <= 0 or count > 20:
        return "Error: count must be between 1 and 20"
    
    if difficulty.lower() not in ["easy", "medium", "hard", "progressive"]:
        return "Error: difficulty must be 'easy', 'medium', 'hard', or 'progressive'"
    
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


# ============================================
# 🚀 SERVER STARTUP
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("🎓 TrainBot MCP Server - Multi-Provider Edition")
    print("=" * 60)
    
    # Check API keys
    print("\n🔑 API Key Status:")
    print(f"  OpenAI:     {'✅ Configured' if os.getenv('OPENAI_API_KEY') else '❌ Missing'}")
    print(f"  Anthropic:  {'✅ Configured' if os.getenv('ANTHROPIC_API_KEY') else '❌ Missing'}")
    print(f"  Gemini:     {'✅ Configured' if os.getenv('GEMINI_API_KEY') else '❌ Missing'}")
    
    print("\n🛠️  Available Tools:")
    print("  1. generate_flashcards - Educational flashcards")
    print("  2. generate_course - Comprehensive courses")
    print("  3. create_quiz - Assessment quizzes")
    print("  4. explain_topic - Detailed explanations")
    print("  5. summarize_content - Content summaries")
    print("  6. create_practice_problems - Practice exercises")
    
    print("\n🤖 Supported AI Providers:")
    print("  • openai (GPT-4o-mini)")
    print("  • anthropic (Claude 3.5 Haiku)")
    print("  • gemini (Gemini 2.0 Flash)")
    
    print("\n" + "=" * 60)
    print("✨ Server starting...\n")
    
    # Run the server
    mcp.run()