# TrainBot Gradio — AI Educational Content Generator (Web Interface)

[![HuggingFace Space](https://img.shields.io/badge/🤗-HuggingFace%20Space-yellow)](YOUR_SPACE_URL_HERE)
[![Status](https://img.shields.io/badge/Status-Production-green)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**Professional web interface for TrainBot's AI-powered educational content generation tools.**

---

## 📚 Overview

TrainBot-Gradio is a standalone web application that provides the same powerful educational content generation tools as [TrainBot-MCP](../TrainBot-MCP), but with a user-friendly web interface accessible to anyone—no MCP knowledge or Claude Desktop required.

**Key Difference from TrainBot-MCP:**
- **TrainBot-MCP:** MCP server for Claude Desktop (technical users)
- **TrainBot-Gradio:** Web app for everyone (educators, students, content creators)
- **Same Tools:** Both use identical AI-powered content generation logic

---

## ✨ Features

### 6 Content Generation Tools

1. **📝 Content Summarizer** — Distill long-form content into executive summaries, detailed summaries, or bullet points
2. **📚 Course Builder** — Create comprehensive multi-module courses with progressive difficulty levels
3. **🔍 Topic Explainer** — Generate in-depth explanations with analogies and real-world examples
4. **🎯 Quiz Creator** — Build assessments with customizable difficulty and automatic answer keys
5. **⚔️ Practice Problems** — Generate progressive practice exercises with detailed solutions
6. **📇 Flashcards Generator** — Create spaced-repetition-ready flashcards for any topic

### Multi-Provider Support

- **OpenAI** (GPT-4o-mini) — Fast, cost-effective, excellent for general content
- **Anthropic** (Claude 3.5 Haiku) — Strong reasoning, great for complex explanations
- **Google Gemini** (2.0 Flash) — Free tier available, good for experimentation

### Professional Interface

- Premium, enterprise-grade design aesthetic
- Distinctive typography (Playfair Display, JetBrains Mono, Inter)
- Refined color palette (obsidian, gold, copper accents)
- Responsive layout optimized for content creation
- Copy-to-clipboard for all outputs

---

## 🚀 Quick Start

### Online (No Installation)

**[Visit Live Demo on HuggingFace Spaces](YOUR_SPACE_URL)**

1. Visit the live demo
2. Select your AI provider
3. Choose a tool tab
4. Enter your parameters
5. Click "Generate"
6. Copy your content

**Note:** You'll need to configure API keys as HuggingFace Secrets if deploying your own instance.

---

## 💻 Local Installation

### Prerequisites

- Python 3.9+
- At least one AI provider API key

### Setup

```bash
# 1. Clone repository
git clone https://github.com/rishi-madhav/mcp-servers.git
cd mcp-servers/TrainBot-Gradio

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

# 5. Run the application
python app.py
```

**Access at:** `http://localhost:7860`

---

## ☁️ Deploy to HuggingFace Spaces

### One-Click Deploy

1. **Create Space:**
   - Go to [HuggingFace Spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose Gradio SDK
   - Name: `trainbot`

2. **Upload Files:**
   - `app.py`
   - `trainbot_tools.py`
   - `requirements.txt`

3. **Configure Secrets:**
   - Settings → Repository Secrets
   - Add secrets:
     - `OPENAI_API_KEY`
     - `ANTHROPIC_API_KEY` (optional)
     - `GEMINI_API_KEY` (optional)

4. **Deploy:**
   - Space auto-deploys on file upload
   - Access at: `https://huggingface.co/spaces/YOUR_USERNAME/trainbot`

---

## 🎯 Use Cases

### For Educators

- Generate comprehensive course materials from scratch
- Create assessments aligned with learning objectives
- Build flashcard decks for student review
- Develop practice problems with detailed solutions

### For Corporate Trainers

- Design onboarding programs
- Create certification courses
- Build assessment libraries
- Generate training documentation

### For Content Creators

- Summarize research papers and articles
- Create educational blog content
- Build online course materials
- Generate supplementary learning resources

### For Students

- Summarize textbook chapters and lecture notes
- Generate practice problems for exam prep
- Create custom flashcards for memorization
- Get detailed explanations with examples

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│     TrainBot Gradio Web Application      │
├─────────────────────────────────────────┤
│                                          │
│  ┌────────────────────────────────┐     │
│  │   Gradio Interface (app.py)    │     │
│  │  • Professional UI/UX          │     │
│  │  • 6 tool tabs                 │     │
│  │  • Provider selector           │     │
│  │  • Copy-to-clipboard           │     │
│  └────────────┬───────────────────┘     │
│               │                          │
│               ▼                          │
│  ┌────────────────────────────────┐     │
│  │  Core Logic (trainbot_tools.py)│     │
│  │  • 6 content generation tools  │     │
│  │  • Multi-provider support      │     │
│  │  • Input validation            │     │
│  │  • Error handling              │     │
│  └────────────┬───────────────────┘     │
│               │                          │
└───────────────┼──────────────────────────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
┌────────┐ ┌─────────┐ ┌──────────┐
│ OpenAI │ │Anthropic│ │  Gemini  │
└────────┘ └─────────┘ └──────────┘
```

---

## 🛠️ Tech Stack

**Frontend:**
- Gradio 5.0.0
- Custom CSS (professional design system)
- Responsive layout

**Backend:**
- Python 3.9+
- OpenAI API (GPT-4o-mini)
- Anthropic API (Claude 3.5 Haiku)
- Google Generative AI (Gemini 2.0 Flash)

**Deployment:**
- HuggingFace Spaces
- Docker (automatic via Gradio SDK)

---

## 📂 File Structure

```
TrainBot-Gradio/
├── app.py                 # Gradio interface with professional UI
├── trainbot_tools.py      # Core AI content generation logic
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .env                  # Your API keys (git-ignored)
├── README.md             # This file
└── venv/                 # Virtual environment (local only)
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# At least one is required
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=AIza...
```

### HuggingFace Secrets

For deployment, add these as Space secrets:
- `OPENAI_API_KEY` (required)
- `ANTHROPIC_API_KEY` (optional)
- `GEMINI_API_KEY` (optional)

---

## 💡 Usage Tips

### Best Practices:

1. **Start Simple:** Test with shorter content first
2. **Choose Right Provider:** OpenAI for speed, Claude for reasoning
3. **Be Specific:** Detailed prompts yield better results
4. **Use Progressive Difficulty:** For practice problems
5. **Copy Early:** Save generated content immediately

### Provider Recommendations:

- **Quick Tasks:** OpenAI (fastest)
- **Complex Explanations:** Anthropic (best reasoning)
- **Experimentation:** Gemini (free tier)

---

## 🧪 Testing

### Local Testing

```bash
# Activate environment
source venv/bin/activate

# Run app
python app.py

# Open browser to http://localhost:7860
```

### Feature Testing

1. Test all 6 tool tabs
2. Try different providers
3. Test edge cases (empty inputs, very long content)
4. Verify copy-to-clipboard functionality

---

## 🐛 Troubleshooting

### "API Key Not Configured" Error

- Check `.env` file exists in project root
- Verify API key format (no quotes, spaces)
- For HuggingFace: Check Space secrets configuration

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Port Already in Use

```bash
# Change port
python app.py --server-port 7861
```

### Slow Generation

- Switch to OpenAI (fastest)
- Reduce content length
- Check internet connection

---

## 🆚 TrainBot-Gradio vs TrainBot-MCP

| Feature | TrainBot-Gradio | TrainBot-MCP |
|---------|-----------------|--------------|
| **Interface** | Web browser | Claude Desktop |
| **Protocol** | Direct API calls | MCP protocol |
| **Target Users** | Everyone | Technical users |
| **Installation** | None (web) / Simple (local) | Requires Claude Desktop |
| **Use Case** | Standalone tool | Integration with Claude |
| **Deployment** | HuggingFace Spaces | Local MCP server |

**Both versions:**
- ✅ Same 6 content generation tools
- ✅ Same multi-provider support
- ✅ Same high-quality outputs
- ✅ Same core AI logic

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional export formats (PDF, DOCX)
- Batch processing
- Content templates
- User accounts and history
- Advanced styling options

**How to Contribute:**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details

---

## 🙏 Acknowledgments

- **Gradio Team** for the excellent web framework
- **OpenAI, Anthropic, Google** for AI APIs
- **HuggingFace** for free hosting platform
- MCP community for feedback

---

## 👤 Author

**Rishi Madhav**

- Location: Bengaluru, India
- GitHub: [@rishi-madhav](https://github.com/rishi-madhav)

---

## 🔗 Related Projects

- [**TrainBot-MCP**](../TrainBot-MCP) — MCP server version for Claude Desktop
- [**StudyBuddy-MCP**](../StudyBuddy-MCP) — Educational assistant (in development)
- [**MCP Servers Collection**](../) — More MCP implementations

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/rishi-madhav/mcp-servers/issues)
- **Discussions:** [GitHub Discussions](https://github.com/rishi-madhav/mcp-servers/discussions)

---

**Built with ❤️ for educators, trainers, and content creators worldwide**
