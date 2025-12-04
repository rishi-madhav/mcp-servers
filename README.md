# MCP Servers Collection

A curated collection of Model Context Protocol (MCP) servers and applications spanning multiple domains and industries.

[![MCP Protocol](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blue)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## 📚 What is MCP?

**Model Context Protocol (MCP)** is an open protocol developed by Anthropic that enables AI assistants to securely connect to external data sources and tools. MCP servers expose capabilities that AI models can use to enhance their responses with real-time information and actions.

**Learn more:** [Official MCP Documentation](https://modelcontextprotocol.io)

---

## 🗂️ Repository Structure

This repository contains multiple MCP server implementations and companion applications:

```
mcp-servers/
├── StudyBuddy-MCP/           # Educational assistant for Indian students
├── TrainBot-MCP/              # AI content generator (MCP server)
├── TrainBot-Gradio/           # TrainBot web interface (Gradio app)
└── [Future Projects]          # More MCP servers coming soon
```

---

## 🚀 Current Projects

### 1. StudyBuddy MCP

**Domain:** Education (K-12, Indian Curricula)

An MCP server providing educational assistance for Indian students following CBSE, ICSE, and IGCSE curricula.

**Features:**
- Curriculum-aligned content for Indian education boards
- Grade-specific learning materials (ages 10-16)
- Subject-specific assistance
- Study planning and resource recommendations

**Status:** 🚧 In Development

[View StudyBuddy README](./StudyBuddy-MCP/README.md)

---

### 2. TrainBot MCP

**Domain:** Education (Professional Training & Content Creation)

An MCP server that generates comprehensive educational content for trainers, educators, and content creators.

**Features:**
- 6 AI-powered content generation tools
- Multi-provider support (OpenAI, Anthropic, Gemini)
- Flashcards, courses, quizzes, explainers, summaries, practice problems
- Integrates seamlessly with Claude Desktop

**Status:** ✅ Production Ready

**MCP 1st Birthday Hackathon:** Track 2 Submission

[View TrainBot-MCP README](./TrainBot-MCP/README.md)

---

### 3. TrainBot Gradio

**Domain:** Education (Web Application)

Companion web interface for TrainBot, making the same powerful tools accessible without MCP knowledge.

**Features:**
- Professional Gradio web interface
- Same 6 content generation tools as TrainBot-MCP
- Multi-provider AI support
- Deployed on HuggingFace Spaces

**Status:** ✅ Production Ready

[View TrainBot-Gradio README](./TrainBot-Gradio/README.md)

---

## 🎯 Why This Repository?

This collection demonstrates MCP's versatility across different use cases:

- **Educational Tools:** StudyBuddy, TrainBot
- **Enterprise Solutions:** Coming soon
- **Productivity Tools:** Coming soon
- **Data Integration:** Coming soon
- **Industry-Specific Solutions:** Coming soon

Each project showcases:
- ✅ Proper MCP protocol implementation
- ✅ Multi-provider AI support where applicable
- ✅ Real-world, production-ready code
- ✅ Comprehensive documentation
- ✅ Best practices for MCP server development

---

## 🛠️ Tech Stack

**MCP Framework:**
- FastMCP 2.13.2+
- Python 3.9+

**AI Providers:**
- OpenAI (GPT models)
- Anthropic (Claude models)
- Google Gemini

**Additional Tools:**
- Gradio (web interfaces)
- Python-dotenv (environment management)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Claude Desktop (for MCP server testing)
- API keys for your chosen AI provider(s)

### Quick Start

1. **Clone the repository:**

```bash
git clone https://github.com/rishi-madhav/mcp-servers.git
cd mcp-servers
```

2. **Choose a project:**

```bash
# For TrainBot MCP server
cd TrainBot-MCP

# For TrainBot web app
cd TrainBot-Gradio

# For StudyBuddy MCP server
cd StudyBuddy-MCP
```

3. **Follow project-specific setup:**
   - Each project has its own README with detailed instructions
   - Install dependencies: `pip install -r requirements.txt`
   - Configure API keys in `.env`
   - Run the server or application

---

## 📖 MCP Server Development Guide

### Creating Your Own MCP Server

Each MCP server in this repository follows a consistent pattern:

```python
from fastmcp import FastMCP

mcp = FastMCP("your-server-name")

@mcp.tool()
def your_tool(param: str) -> str:
    """Tool description for AI to understand"""
    # Your implementation
    return result

if __name__ == "__main__":
    mcp.run()
```

### Best Practices

1. **Clear Tool Descriptions:** Help AI understand what your tool does
2. **Input Validation:** Always validate and sanitize inputs
3. **Error Handling:** Provide meaningful error messages
4. **Type Hints:** Use Python type hints for better tool discovery
5. **Documentation:** Include comprehensive docstrings

---

## 🤝 Contributing

Contributions are welcome! Whether it's:
- New MCP server implementations
- Improvements to existing servers
- Bug fixes or documentation updates
- New domain/industry applications

**How to Contribute:**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📋 Project Roadmap

### Q1 2025

- ✅ TrainBot MCP (Complete)
- ✅ TrainBot Gradio (Complete)
- 🚧 StudyBuddy MCP (In Progress)
- 📋 TrainBot 2.0 (Content ingestion, curriculum design)

### Q2 2025

- 📋 Enterprise data connector MCP servers
- 📋 Productivity tool integrations
- 📋 Industry-specific solutions (healthcare, finance, legal)

### Future

- 📋 MCP server templates and starter kits
- 📋 Multi-server orchestration examples
- 📋 Advanced RAG implementations

---

## 📄 License

This repository is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Individual projects may have additional licensing terms - check project-specific READMEs.

---

## 🙏 Acknowledgments

- **Anthropic** for developing the MCP protocol and hosting the MCP 1st Birthday Hackathon
- **FastMCP** team for the excellent Python framework
- **Gradio** team for making web interfaces simple
- The open-source community for inspiration and support

---

## 👤 Author

**Rishi Madhav**

- 📍 Location: Bengaluru, India
- 💼 Focus: AI application development, educational technology
- 🔗 GitHub: [@rishi-madhav](https://github.com/rishi-madhav)

---

## 📞 Support & Contact

- **Issues:** [GitHub Issues](https://github.com/rishi-madhav/mcp-servers/issues)
- **Discussions:** [GitHub Discussions](https://github.com/rishi-madhav/mcp-servers/discussions)

---

## 🌟 Star History

If you find these MCP servers useful, please consider starring the repository! ⭐

---

**Built with ❤️ for the MCP community**
