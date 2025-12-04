# TrainBot MCP — AI Educational Content Generator

[![MCP Server](https://img.shields.io/badge/MCP-Server-blue)](https://modelcontextprotocol.io)
[![Status](https://img.shields.io/badge/Status-Production-green)]()
[![MCP Hackathon](https://img.shields.io/badge/MCP-1st%20Birthday%20Hackathon-purple)](https://lu.ma/mcp-hackathon)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

**Professional-grade MCP server for generating comprehensive educational content. Built for the MCP 1st Birthday Hackathon (Track 2).**

---

## 📚 Overview

TrainBot-MCP is a Model Context Protocol server that provides AI-powered educational content generation tools through Claude Desktop. It enables educators, trainers, and content creators to generate high-quality learning materials using their choice of AI provider.

**Track 2 Submission:** Building with MCP Servers

**Companion Project:** [TrainBot-Gradio](../TrainBot-Gradio) (web interface)

---

## ✨ Features

### 6 Content Generation Tools

All tools are exposed via the MCP protocol and accessible through Claude Desktop:

1. **📇 generate_flashcards** — Create educational flashcards with customizable difficulty
2. **📚 generate_course** — Build comprehensive multi-module courses
3. **🎯 create_quiz** — Generate assessments with optional answer keys
4. **🔍 explain_topic** — Produce detailed explanations with analogies
5. **📝 summarize_content** — Distill long-form content into summaries
6. **⚔️ create_practice_problems** — Generate practice exercises with solutions

### Multi-Provider Support

Choose your AI provider for each tool call:
- **OpenAI** (GPT-4o-mini) — Fast, cost-effective
- **Anthropic** (Claude 3.5 Haiku) — Strong reasoning
- **Google Gemini** (2.0 Flash) — Free tier available

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│        Claude Desktop (MCP Client)       │
└───────────────┬─────────────────────────┘
                │ MCP Protocol (STDIO)
                ▼
┌─────────────────────────────────────────┐
│         TrainBot MCP Server              │
│  ┌─────────────────────────────────┐    │
│  │  FastMCP Framework              │    │
│  ├─────────────────────────────────┤    │
│  │  6 Educational Tools            │    │
│  │  • generate_flashcards          │    │
│  │  • generate_course              │    │
│  │  • create_quiz                  │    │
│  │  • explain_topic                │    │
│  │  • summarize_content            │    │
│  │  • create_practice_problems     │    │
│  └─────────────────────────────────┘    │
└───────────────┬─────────────────────────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
┌────────┐ ┌─────────┐ ┌──────────┐
│ OpenAI │ │Anthropic│ │  Gemini  │
└────────┘ └─────────┘ └──────────┘
```

---

## 🚀 Installation

### Prerequisites

- Python 3.9+
- Claude Desktop
- At least one AI provider API key

### Setup Steps

```bash
# 1. Clone repository
git clone https://github.com/rishi-madhav/mcp-servers.git
cd mcp-servers/TrainBot-MCP

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
# Edit .env with your API keys:
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# GEMINI_API_KEY=AIza...
```

### Claude Desktop Configuration

Edit your Claude Desktop config file:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "trainbot": {
      "command": "/absolute/path/to/TrainBot-MCP/venv/bin/python",
      "args": ["/absolute/path/to/TrainBot-MCP/trainbot_server.py"]
    }
  }
}
```

**Important:** Use absolute paths, not relative paths or `~`.

### Launch

1. Restart Claude Desktop
2. Look for the 🔌 icon in the bottom-right
3. Verify "trainbot" server is connected
4. Available tools will appear automatically

---

## 🎯 Usage Examples

### Example 1: Generate Flashcards

**In Claude Desktop:**

```
User: "Use TrainBot to generate 10 flashcards about Machine Learning basics"

Claude: [Calls generate_flashcards tool with parameters]
       topic="Machine Learning basics"
       count=10
       level="intermediate"
       ai_provider="openai"
```

### Example 2: Create a Course

```
User: "Create a 5-module Python programming course for beginners, 2 weeks duration"

Claude: [Calls generate_course tool]
       title="Python Programming Fundamentals"
       modules=5
       level="beginner"
       duration="2 weeks"
       ai_provider="anthropic"
```

### Example 3: Generate Quiz

```
User: "Make a 15-question quiz on Data Structures, mixed difficulty, with answers"

Claude: [Calls create_quiz tool]
       topic="Data Structures"
       questions=15
       difficulty="mixed"
       include_answers=true
       ai_provider="openai"
```

---

## 🛠️ Tool Reference

### 1. generate_flashcards

```python
generate_flashcards(
    topic: str,              # Topic for flashcards
    count: int = 10,         # Number of cards (1-50)
    level: str = "intermediate",  # beginner/intermediate/advanced
    ai_provider: str = "openai"   # openai/anthropic/gemini
) -> str
```

### 2. generate_course

```python
generate_course(
    title: str,              # Course title
    modules: int = 5,        # Number of modules (1-15)
    level: str = "intermediate",  # beginner/intermediate/advanced
    duration: str = "1 week",     # Course duration
    ai_provider: str = "openai"
) -> str
```

### 3. create_quiz

```python
create_quiz(
    topic: str,              # Quiz topic
    questions: int = 10,     # Number of questions (1-30)
    difficulty: str = "mixed",    # easy/medium/hard/mixed
    include_answers: bool = True, # Include answer key
    ai_provider: str = "openai"
) -> str
```

### 4. explain_topic

```python
explain_topic(
    topic: str,              # Topic to explain
    depth: str = "comprehensive",  # brief/comprehensive/detailed
    use_analogies: bool = True,    # Include analogies
    ai_provider: str = "openai"
) -> str
```

### 5. summarize_content

```python
summarize_content(
    content: str,            # Content to summarize
    summary_type: str = "executive",  # executive/detailed/bullet_points
    max_length: str = "medium",       # short/medium/long
    ai_provider: str = "openai"
) -> str
```

### 6. create_practice_problems

```python
create_practice_problems(
    topic: str,              # Problem topic
    count: int = 5,          # Number of problems (1-20)
    difficulty: str = "progressive",  # easy/medium/hard/progressive
    include_solutions: bool = True,   # Include solutions
    ai_provider: str = "openai"
) -> str
```

---

## 💡 Tips & Best Practices

### For Best Results:

1. **Be Specific:** Provide clear, detailed topics
2. **Choose Appropriate Level:** Match to your target audience
3. **Use Progressive Difficulty:** For practice problems
4. **Include Answers:** Essential for self-study materials
5. **Select Right Provider:** OpenAI for speed, Claude for reasoning

### Common Use Cases:

- **Corporate Training:** Generate onboarding materials
- **Academic Courses:** Create comprehensive curricula
- **Exam Prep:** Build practice quizzes and problems
- **Content Creation:** Produce educational blog posts
- **Student Support:** Generate study guides and flashcards

---

## 📊 API Costs (Approximate)

| Provider | Model | Input Cost | Output Cost | Best For |
|----------|-------|------------|-------------|----------|
| OpenAI | GPT-4o-mini | $0.15/1M tokens | $0.60/1M tokens | Speed, Cost |
| Anthropic | Claude 3.5 Haiku | $0.25/1M tokens | $1.25/1M tokens | Reasoning |
| Gemini | 2.0 Flash | Free tier | Free tier | Testing |

**Note:** Costs are approximate. Check provider pricing pages for current rates.

---

## 🔧 Technical Details

### Dependencies

```
fastmcp==2.13.2
openai==1.54.0
anthropic==0.39.0
google-generativeai==0.8.3
python-dotenv==1.0.1
```

### Python Version

- Minimum: Python 3.9
- Recommended: Python 3.11+

### File Structure

```
TrainBot-MCP/
├── trainbot_server.py      # Main MCP server
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── .env                   # Your API keys (git-ignored)
├── venv/                  # Virtual environment
└── README.md              # This file
```

---

## 🧪 Testing

### Test the Server

```bash
# Activate virtual environment
source venv/bin/activate

# Run server directly (for testing)
python trainbot_server.py

# Should output:
# 🎓 TrainBot MCP Server - Multi-Provider Edition
# 🔑 API Key Status: ...
# 🛠️ Available Tools: [6 tools]
```

### Test with Claude Desktop

1. Configure server in Claude Desktop
2. Restart Claude Desktop
3. Look for 🔌 connection indicator
4. Try: "Use TrainBot to generate 3 flashcards about Python"

---

## 🐛 Troubleshooting

### Server Not Connecting

- Check absolute paths in Claude config
- Verify virtual environment Python path
- Restart Claude Desktop
- Check logs in Claude Desktop console

### API Key Errors

- Verify `.env` file exists in TrainBot-MCP directory
- Check API key format (no quotes, no spaces)
- Test keys with provider's official tools
- Ensure `.env` is not git-committed

### Import Errors

- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (need 3.9+)

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional content types (case studies, simulations)
- More AI provider integrations
- Enhanced error handling
- Performance optimizations

---

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details

---

## 🙏 Acknowledgments

- **Anthropic** for the MCP protocol and hackathon
- **FastMCP** team for the excellent framework
- **OpenAI, Anthropic, Google** for AI APIs
- MCP community for feedback and support

---

## 👤 Author

**Rishi Madhav**

- Location: Bengaluru, India
- GitHub: [@rishi-madhav](https://github.com/rishi-madhav)
- Project: MCP 1st Birthday Hackathon - Track 2

---

## 🔗 Related Projects

- [**TrainBot-Gradio**](../TrainBot-Gradio) — Web interface version
- [**StudyBuddy-MCP**](../StudyBuddy-MCP) — Educational assistant (in development)

---

**Built for the MCP 1st Birthday Hackathon | Track 2: Building with MCP Servers**
