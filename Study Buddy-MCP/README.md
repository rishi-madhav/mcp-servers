# StudyBuddy MCP — AI Educational Assistant for Indian Students

[![MCP Server](https://img.shields.io/badge/MCP-Server-blue)](https://modelcontextprotocol.io)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange)]()
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

**An MCP server providing educational assistance for Indian students (ages 10-16) following CBSE, ICSE, and IGCSE curricula.**

---

## 📚 Overview

StudyBuddy is a specialized MCP server designed to assist Indian K-12 students with their studies. It provides curriculum-aligned content, study planning, and educational resources tailored to the Indian education system.

**Target Audience:**
- Indian students aged 10-16
- Following CBSE, ICSE, or IGCSE curricula
- Parents seeking study support for their children
- Teachers looking for supplementary resources

---

## ✨ Features (Planned)

### Core Capabilities

- 📖 Curriculum-aligned explanations (CBSE/ICSE/IGCSE)
- 📝 Subject-specific assistance (Math, Science, Social Studies, Languages)
- 🎯 Grade-appropriate content (Classes 5-10)
- 📅 Study planning and schedule recommendations
- 🔍 Concept clarification with Indian context
- 📚 Resource recommendations (textbooks, reference materials)

### External Integrations

- Wikipedia for background knowledge
- Khan Academy for video tutorials
- YouTube Educational content (curated)
- NCERT/ICSE/IGCSE official resources

### Advanced Features (Future)

- RAG (Retrieval-Augmented Generation) for curriculum content
- Exam preparation assistance
- Practice problem generation
- Progress tracking

---

## 🏗️ Architecture

```
StudyBuddy MCP Server
├── MCP Protocol (STDIO)
├── Core Tools
│   ├── explain_concept(topic, grade, subject, curriculum)
│   ├── generate_practice_questions(topic, difficulty, count)
│   ├── suggest_study_plan(subjects, exam_date, current_level)
│   └── recommend_resources(topic, grade, curriculum)
├── External Context
│   ├── Wikipedia search
│   ├── Khan Academy search
│   └── YouTube educational content
└── AI Provider (Gemini 2.0 Flash)
```

---

## 🚀 Installation (Coming Soon)

### Prerequisites

- Python 3.9+
- Claude Desktop
- Google Gemini API key

### Setup

```bash
# Clone repository
git clone https://github.com/rishi-madhav/mcp-servers.git
cd mcp-servers/StudyBuddy-MCP

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your GEMINI_API_KEY
```

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "studybuddy": {
      "command": "/path/to/StudyBuddy-MCP/venv/bin/python",
      "args": ["/path/to/StudyBuddy-MCP/studybuddy_server.py"]
    }
  }
}
```

---

## 🎯 Use Cases

### For Students

- Get explanations of difficult concepts in simple language
- Practice problems aligned with your curriculum
- Study schedule based on upcoming exams
- Find quality educational resources

### For Parents

- Help children with homework
- Find appropriate study materials
- Track learning progress
- Understand curriculum requirements

### For Teachers

- Supplement classroom teaching
- Find additional resources for students
- Generate practice questions
- Provide personalized assistance to struggling students

---

## 🛠️ Tech Stack

- **Framework:** FastMCP 2.13.2
- **AI Provider:** Google Gemini 2.0 Flash
- **Python:** 3.9+
- **External APIs:** Wikipedia, Khan Academy, YouTube

---

## 📋 Development Status

**Current Phase:** 🚧 Active Development

**Completed:**
- ✅ Project planning and architecture
- ✅ Curriculum research (CBSE/ICSE/IGCSE)

**In Progress:**
- 🚧 Core MCP server implementation
- 🚧 External context integrations
- 🚧 RAG system for curriculum content

**Upcoming:**
- 📋 Testing with real students
- 📋 Additional features based on feedback
- 📋 Web interface (Gradio app)

---

## 🤝 Contributing

This project is actively seeking contributors, especially:
- Educators familiar with Indian curricula
- Students who can provide feedback
- Developers interested in EdTech

**How to Help:**

1. Test the server with real student queries
2. Provide feedback on content accuracy
3. Suggest new features
4. Report bugs or issues

---

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details

---

## 🙏 Acknowledgments

- Indian education boards (CBSE, ICSE, CISCE) for curriculum standards
- Khan Academy for educational content
- Wikipedia for knowledge resources
- Students and educators who provided input

---

## 👤 Author

**Rishi Madhav**

- Location: Bengaluru, India
- GitHub: [@rishi-madhav](https://github.com/rishi-madhav)

---

## 📞 Support

For questions or feedback:
- Open an issue: [GitHub Issues](https://github.com/rishi-madhav/mcp-servers/issues)
- Tag: `studybuddy-mcp`

---

**Status:** Coming Soon | Expected Launch: Q1 2025
