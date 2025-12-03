# 🚀 IMMEDIATE SETUP - DO THIS NOW!

## Step 1: Download Files (1 minute)

Download these 4 files to your `trainbot-voice` folder:
1. app.py
2. document_processor.py  
3. course_generator.py
4. requirements.txt

Also download: env_template.txt (rename to .env)

---

## Step 2: Create .env File (2 minutes)

Create a file called `.env` in your trainbot-voice folder with:

```
GEMINI_API_KEY=your_actual_gemini_api_key
ELEVENLABS_API_KEY=your_actual_elevenlabs_key  
OPENAI_API_KEY=your_actual_openai_key
```

**IMPORTANT:** Replace the "your_actual..." parts with your REAL API keys!

---

## Step 3: Install Libraries (if not done) (2 minutes)

```bash
cd trainbot-voice
pip install -r requirements.txt
```

---

## Step 4: RUN IT! (1 minute)

```bash
python app.py
```

Your browser should open to: http://127.0.0.1:7860

---

## Step 5: TEST IT (5 minutes)

### Test 1: Upload a PDF
1. Go to "Step 1: Upload Materials"
2. Click to upload a PDF (any PDF!)
3. Click "Process Document"
4. You should see: "✅ Successfully processed!"

### Test 2: Ask a Question  
1. Go to "Step 2: Explore Content"
2. Type: "What is this document about?"
3. Press Enter
4. You should get an AI answer from Gemini!

### Test 3: Generate Course
1. Go to "Step 3: Generate Course"
2. Type a topic: "Training Course"
3. Click "Generate Course Outline"
4. You should see a full course outline!

---

## ✅ IF IT WORKS:

**CELEBRATE!** 🎉 You just built an AI-powered app!

**Now tell me:** "It works! What's next?"

---

## ❌ IF YOU GET ERRORS:

### Error: "GEMINI_API_KEY not found"
- Check your .env file exists
- Check the API keys are correct (no quotes, no spaces)
- Make sure .env is in the same folder as app.py

### Error: "No module named 'gradio'"
- Run: `pip install -r requirements.txt`

### Error: "Invalid API key"
- Double-check you copied the keys correctly
- Make sure no extra spaces or quotes
- Try regenerating the API key

### Other Errors:
- Copy the FULL error message
- Send it to me
- I'll help you fix it!

---

## 📊 YOUR FOLDER STRUCTURE SHOULD LOOK LIKE:

```
trainbot-voice/
├── .env                    (your API keys)
├── app.py                  (main app)
├── document_processor.py   (PDF processing + Gemini Q&A)
├── course_generator.py     (course generation)
└── requirements.txt        (libraries)
```

---

## ⏰ TIME CHECK:

You should complete this in 10-15 minutes.

**By 1:30 PM you should have:** A working AI app! ✅

---

## 🎯 NEXT: Once Working

After you confirm it works, we'll add:
- Voice input (Whisper)
- Voice output (ElevenLabs)  
- Better UI polish
- Deploy to Modal

**But first, let's get Day 1 version working!**

---

**GO GO GO!** 🔥

Download the files, set up .env, run `python app.py`!

Tell me when it's running! 🚀
