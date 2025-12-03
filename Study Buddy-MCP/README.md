# 🎓 StudyBuddy - AI-Powered Study Companion

> Your intelligent study companion for CBSE/ICSE/IGCSE students (Grades 5-10)

Built for the **MCP 1st Birthday Hackathon** with ❤️

![Powered by Google Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4?style=for-the-badge)
![Built with MCP](https://img.shields.io/badge/Built%20with-MCP-000000?style=for-the-badge)
![Gradio](https://img.shields.io/badge/UI-Gradio-FF6F00?style=for-the-badge)

## ✨ Features

### 🔧 MCP Server Tools

1. **📚 Explain Topic** - Get grade-appropriate explanations aligned with your curriculum
2. **✏️ Generate Practice** - Create custom practice problems with varying difficulty
3. **🔍 Solve Step-by-Step** - Detailed solutions for math/science problems
4. **📖 Create Story** - Transform boring topics into engaging stories
5. **🎯 Quiz Me** - 10-question quizzes with intelligent question tracking (no repeats!)

### 💎 Key Capabilities

- ✅ **Curriculum Aligned**: CBSE, ICSE, and IGCSE standards
- ✅ **Grade Adaptive**: Content tailored for grades 5-10
- ✅ **Smart Memory**: Tracks learning history and avoids duplicate quiz questions
- ✅ **Dual Interface**: Both MCP tools (for Claude Desktop) and Gradio web UI
- ✅ **Structured Output**: All responses in clean JSON format

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Claude Desktop (optional, for MCP integration)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd studybuddy-mcp

# Run setup script
chmod +x setup.sh
./setup.sh

# Edit .env and add your API key
nano .env  # or use your preferred editor
```

### Configuration

1. **Add your Gemini API key** to `.env`:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

2. **For Claude Desktop integration** (optional):
```bash
# Copy the MCP config to Claude Desktop
# On Mac:
cp claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Don't forget to update the GEMINI_API_KEY in the config!
```

### Running the App

```bash
# Activate virtual environment
source .venv/bin/activate

# Launch Gradio interface
python gradio_app/app.py
```

Open http://localhost:7860 in your browser 🎉

## 📖 Usage

### Via Gradio Interface

1. **Set up your profile**: Enter name, select grade (5-10) and board (CBSE/ICSE/IGCSE)
2. **Choose a tool** from the tabs:
   - Explain Topic
   - Practice Problems
   - Solve Problem
   - Story Mode
   - Quiz Me
3. **View your progress** in the "My Progress" tab

### Via Claude Desktop (MCP)

Once configured, you can ask Claude:

```
"Explain photosynthesis for a grade 8 CBSE student"
"Generate 5 practice problems on quadratic equations for grade 10"
"Create a fun story about the water cycle"
"Quiz me on cell division (grade 9 ICSE)"
```

## 🏗️ Architecture

```
studybuddy-mcp/
├── mcp_server/
│   ├── server.py         # MCP server with 5 tools
│   ├── database.py       # SQLite for history tracking
│   ├── prompts.py        # Structured prompts for Gemini
│   └── gemini_client.py  # Google Gemini API integration
├── gradio_app/
│   └── app.py           # Enterprise-grade Gradio UI
├── data/
│   └── studybuddy.db    # Student progress database
└── README.md
```

### Tech Stack

- **MCP Server**: Python FastMCP framework
- **LLM**: Google Gemini 1.5 Flash (fast, cost-effective)
- **Database**: SQLite with async support (aiosqlite)
- **Frontend**: Gradio 5 with custom enterprise CSS
- **Deployment**: Modal (coming soon)

## 🎯 Sponsor Integration

### Google Gemini ✅
- All content generation powered by Gemini 1.5 Flash
- Structured JSON outputs for reliable parsing
- Cost-effective for educational use cases

### Modal ⏳
- Deployment configuration coming soon
- Serverless scaling for student workloads

### ElevenLabs 🔜
- Audio explanations (if time permits)
- Text-to-speech for accessibility

## 📊 Database Schema

```sql
students          # Student profiles
├── id, name, grade, board, created_at

explained_topics  # Topic explanations history
├── id, student_id, subject, topic, explanation, timestamp

practice_problems # Generated practice sets
├── id, student_id, subject, topic, problems (JSON), timestamp

quiz_history     # Quiz attempts with scores
├── id, student_id, subject, topic, questions (JSON), score, timestamp
```

## 🛠️ Development

### Running Tests

```bash
# Test MCP server with MCP Inspector
npx @modelcontextprotocol/inspector python -m mcp_server.server

# Test database operations
python -c "
import asyncio
from mcp_server import database
asyncio.run(database.init_database())
print('✅ Database test passed')
"
```

### Adding New Tools

1. Add prompt template in `mcp_server/prompts.py`
2. Register tool in `mcp_server/server.py`
3. Add handler function
4. Update Gradio UI in `gradio_app/app.py`

## 🎓 Educational Impact

StudyBuddy addresses key challenges in Indian education:

- **Personalization**: Adapts to student's grade and board
- **Accessibility**: Free AI tutoring for all students
- **Engagement**: Stories make learning fun
- **Practice**: Unlimited custom problems
- **Progress Tracking**: Students see their growth

## 🏆 Hackathon Submission

**Track**: Building MCP (Track 1)
**Category**: Productivity Tools
**Special Awards**: Google Gemini, Modal Innovation

**Demo Video**: [Link coming soon]
**Social Post**: [Link coming soon]

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Anthropic** for Claude and MCP protocol
- **Google** for Gemini API
- **Gradio** for the amazing UI framework
- **Modal** for deployment platform

## 🔗 Links

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Google Gemini API](https://ai.google.dev/)
- [Gradio Docs](https://www.gradio.app/)

---

**Made with ❤️ for students by students**

*Have feedback? Open an issue or reach out!*
