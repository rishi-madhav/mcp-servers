# 🎓 TrainBot - AI Training Course Generator

**MCP 1st Birthday Hackathon Submission**  
**Track:** Agent Application - Productivity Category  
**Tags:** `agent-app-track-productivity`

---

## 🌟 What It Does

TrainBot helps organizations create professional training courses from existing materials (PDFs, presentations, videos). Simply upload your documents and let AI:

- 📤 **Process multiple document types** (PDF, PowerPoint)
- 💬 **Answer questions** about your training materials
- 📚 **Auto-generate course outlines** with modules, objectives, and assessments

**Perfect for:** Product training, employee onboarding, customer enablement, internal documentation

---

## 🎯 Problem It Solves

Many organizations have scattered training materials but lack structured courses. Creating comprehensive training programs manually is time-consuming and requires instructional design expertise. TrainBot automates this process, saving hours of work.

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Download these files:**
   - `app.py`
   - `document_processor.py`
   - `course_generator.py`
   - `requirements.txt`

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   - The app will automatically open at `http://localhost:7860`
   - If not, click the URL shown in your terminal

That's it! You're ready to use TrainBot! 🎉

---

## 📖 How to Use

### Step 1: Upload Materials
1. Go to the "📤 Upload Materials" tab
2. Click to upload a PDF or PowerPoint file
3. Click "Process Document"
4. Wait for confirmation

### Step 2: Ask Questions
1. Go to the "💬 Ask Questions" tab
2. Type your question in the chat box
3. Get AI-powered answers based on your documents

### Step 3: Generate Course
1. Go to the "📚 Generate Course" tab
2. Enter a course topic (e.g., "Product Overview")
3. Choose number of modules (3-10)
4. Click "Generate Course Outline"
5. Review your auto-generated training course!

---

## 🏗️ Project Structure

```
trainbot/
├── app.py                    # Main Gradio interface (the UI)
├── document_processor.py     # Handles file uploads and Q&A
├── course_generator.py       # Creates course outlines
└── requirements.txt          # Python dependencies
```

**Total lines of code:** ~350 (beginner-friendly!)

---

## 🎓 For Non-Developers

This is a **starter template** designed to be easy to understand and modify:

- ✅ Each file has extensive comments explaining what it does
- ✅ Simple, readable code (no complex frameworks)
- ✅ Modular structure - change one file without breaking others
- ✅ Mock data for demo purposes (easy to test)

**Want to customize?** Just ask Claude or another AI assistant:
- "Add a file upload progress bar"
- "Change the color scheme to blue"
- "Add a download button for the course outline"

---

## 🔮 Future Enhancements

This starter version uses mock data. The production version will include:

- ✅ **Real PDF/PowerPoint extraction** (PyPDF2, python-pptx)
- ✅ **AI-powered Q&A** (OpenAI/Anthropic API integration)
- ✅ **Semantic search** (ChromaDB vector database)
- ✅ **Video transcription** (Whisper API)
- ✅ **MCP servers** for document processing
- ✅ **Quiz generation** from content
- ✅ **Progress tracking** for learners
- ✅ **Export to PDF/DOCX** formats

---

## 🔒 Security & Privacy

**For Demo:** Uses mock data (safe for public showcase)

**For Production:** 
- Deploy privately on your infrastructure
- No data sent to external services
- Full control over document storage
- Compatible with air-gapped environments

---

## 💰 Hackathon Submission Details

**Track:** Track 2 - Agent Application (Productivity Category)  
**Category:** Productivity (workflow automation for training/enablement)  
**Team Size:** Solo  
**Development Time:** 17 days (Nov 14-30, 2025)

**Key Features Demonstrated:**
- ✅ Autonomous agent behavior (document analysis, course generation)
- ✅ Multi-modal input (PDFs, presentations)
- ✅ Practical productivity application
- ✅ Polished Gradio 6 interface
- ✅ Real-world business value

---

## 📱 Social Media

[Add your social media post link here before submission!]

**Example post:**
> "Built TrainBot for the #MCP1stBirthday hackathon! 🎓 
> 
> Upload training materials → AI generates complete courses with modules, objectives & assessments.
> 
> Perfect for product enablement & employee onboarding. Built with @Gradio in 2 weeks!
> 
> Try it: [your-space-link]"

---

## 🎥 Demo Video

[Add your 1-5 minute demo video link here before submission!]

**What to show in your video:**
1. Quick intro (15 sec) - what problem does it solve?
2. Upload a document (30 sec)
3. Ask a few questions (45 sec)
4. Generate a course outline (60 sec)
5. Show the results (30 sec)
6. Closing thoughts (30 sec)

**Total:** 3-4 minutes

---

## 🛠️ Tech Stack

- **Framework:** Gradio 6
- **Language:** Python 3.8+
- **UI Theme:** Gradio Soft Theme
- **Deployment:** Hugging Face Spaces

---

## 📚 Resources Used

- [Gradio Documentation](https://www.gradio.app)
- [MCP Hackathon Guidelines](https://huggingface.co/MCP-1st-Birthday)
- [Gradio + MCP Tutorial](https://huggingface.co/blog/gradio-mcp)

---

## 👤 About the Creator

[Add a sentence about yourself and why you built this!]

Example:
> "I'm a [your role] at [company] frustrated with the lack of good training materials for our product. I built TrainBot to solve this problem and learned Gradio in the process! This is my first hackathon submission."

---

## 🙏 Acknowledgments

- Anthropic & Gradio for organizing this amazing hackathon
- The MCP community for inspiration
- Claude AI for helping with code and guidance

---

## 📄 License

MIT License - Feel free to use and modify for your own projects!

---

**Built with ❤️ for the MCP 1st Birthday Hackathon**

*Questions? Find me on [Discord](https://discord.gg/fveShqytyh) in #agents-mcp-hackathon-winter25🏆*
