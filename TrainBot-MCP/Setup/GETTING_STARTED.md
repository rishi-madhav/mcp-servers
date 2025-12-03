# 🎯 GETTING STARTED - For Complete Beginners

Hi! This guide will help you get TrainBot running on your computer in 10 minutes, even if you've never coded before.

---

## ⚙️ STEP 1: Install Python (5 minutes)

### For Windows:
1. Go to https://www.python.org/downloads/
2. Click the big yellow "Download Python" button
3. Run the installer
4. ⚠️ **IMPORTANT:** Check the box that says "Add Python to PATH"
5. Click "Install Now"
6. Wait for it to finish

### For Mac:
1. Go to https://www.python.org/downloads/
2. Download the macOS installer
3. Open the downloaded file
4. Follow the installation steps

### Verify it worked:
1. Open Terminal (Mac) or Command Prompt (Windows)
   - **Windows:** Press Windows key, type "cmd", press Enter
   - **Mac:** Press Cmd+Space, type "terminal", press Enter
2. Type: `python --version`
3. You should see something like "Python 3.11.5"

✅ **If you see a version number, you're good to go!**

---

## 📥 STEP 2: Download the Files (2 minutes)

You need to download these 5 files:
1. `app.py`
2. `document_processor.py`
3. `course_generator.py`
4. `requirements.txt`
5. `README.md`

### Option A: Download from Claude
The files are already created above - ask me to package them for download!

### Option B: Manual Creation
1. Create a new folder called "trainbot" on your Desktop
2. Open a text editor (Notepad on Windows, TextEdit on Mac)
3. Copy each file content from above
4. Save each file with the exact name shown
5. Save all files in your "trainbot" folder

**Your folder should look like:**
```
Desktop/
└── trainbot/
    ├── app.py
    ├── document_processor.py
    ├── course_generator.py
    ├── requirements.txt
    └── README.md
```

---

## 🚀 STEP 3: Install Gradio (2 minutes)

1. Open Terminal/Command Prompt
2. Navigate to your trainbot folder:
   - **Windows:** `cd Desktop\trainbot`
   - **Mac:** `cd Desktop/trainbot`
3. Type this command and press Enter:
   ```
   pip install -r requirements.txt
   ```
4. Wait for it to download and install (takes 1-2 minutes)
5. You should see "Successfully installed gradio..."

✅ **If you see "Successfully installed", you're ready!**

---

## ▶️ STEP 4: Run the App (1 minute)

1. In the same Terminal/Command Prompt window, type:
   ```
   python app.py
   ```
2. Press Enter
3. Wait 5-10 seconds
4. You'll see some messages, and then:
   ```
   Running on local URL: http://127.0.0.1:7860
   ```
5. Your browser might open automatically
6. If not, copy that URL and paste it in your browser

🎉 **You should now see TrainBot running!**

---

## 🎮 STEP 5: Test It Out (2 minutes)

1. **Upload Tab:** Try clicking "Upload PDF or PowerPoint" (even if you don't have files yet)
2. **Ask Questions Tab:** Type "What are the main features?" and press Enter
3. **Generate Course Tab:** Type "Product Training" and click "Generate Course Outline"

You'll see mock responses because we're using sample data. That's perfect for learning!

---

## 🆘 Troubleshooting

### "Python is not recognized..."
- You forgot to check "Add Python to PATH" during installation
- Solution: Uninstall Python and reinstall with PATH checked

### "No module named 'gradio'"
- The pip install didn't work
- Solution: Try `pip3 install -r requirements.txt` instead

### "Address already in use"
- Something else is using port 7860
- Solution: Change the last line in app.py to:
  ```python
  demo.launch(share=False, server_port=7861)
  ```

### App won't load in browser
- Try typing the URL manually: `http://localhost:7860`
- Try a different browser (Chrome usually works best)

### Still stuck?
- Post in the Discord: https://discord.gg/fveShqytyh
- Channel: #agents-mcp-hackathon-winter25🏆
- Or ask me (Claude) for help!

---

## 📝 Next Steps After You Get It Running

### Week 1 Goals:
- ✅ Get the app running (you just did this!)
- ⏭️ Play with the interface - click everything
- ⏭️ Read through app.py to understand the structure
- ⏭️ Make a small change (like the title) to see how it works
- ⏭️ Watch some Gradio tutorials on YouTube

### Week 2 Goals:
- Add real PDF processing
- Connect to an AI API (OpenAI or Anthropic)
- Polish the UI
- Record your demo video
- Submit to the hackathon!

**I'll help you with each step!** Just ask:
- "How do I change the color scheme?"
- "Help me add real PDF processing"
- "I want to add a logo"
- etc.

---

## 💡 Learning Resources

**Gradio Basics (watch these!):**
- Gradio Quick Start: https://www.gradio.app/guides/quickstart
- YouTube: "Gradio Tutorial for Beginners"
- Official Docs: https://www.gradio.app

**Python Basics (if needed):**
- Python for Beginners: https://www.python.org/about/gettingstarted/
- YouTube: "Python in 10 minutes"

**AI Coding Assistants (to help you code):**
- Claude (you're already here!)
- Cursor: https://cursor.sh
- GitHub Copilot: https://github.com/features/copilot

---

## 🎯 Your Mission (If You Choose to Accept It)

**By November 30:**
1. ✅ Get the starter template running (you're here!)
2. Customize it with your ideas
3. Make it look professional
4. Add at least one "real" feature (PDF extraction or AI Q&A)
5. Record a demo video
6. Submit to hackathon
7. (Optionally) Win prizes! 💰

**You got this!** 🚀

Remember: The hackathon judges care about:
- Does it work?
- Does it solve a real problem?
- Is the UI nice?
- Is it useful?

They DON'T care about:
- Perfect code
- Complex architecture
- How much experience you have

So focus on making something that WORKS and looks GOOD. 
The code can be simple - that's totally fine!

---

**Questions?** Just ask me anytime. I'm your coding buddy for this hackathon! 🤝

Good luck! 🍀
