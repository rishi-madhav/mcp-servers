# 🎙️ VOICE FEATURES - SETUP & TESTING GUIDE

## 📦 STEP 1: INSTALL NEW LIBRARIES (5 mins)

```bash
pip install elevenlabs
pip install sounddevice soundfile numpy
```

**If you already have moviepy installed:**
- You're good to go!

**If not:**
```bash
pip install moviepy imageio-ffmpeg
```

---

## 📥 STEP 2: DOWNLOAD FILES (2 mins)

Download these 2 NEW files:
1. **app_WITH_VOICE.py** → Rename to `app.py`
2. **voice_processor.py** → Keep this name

Plus keep your existing:
- `document_processor.py` (with video support)
- `course_generator.py` (with skill levels)
- `.env` (with all API keys)

---

## 🔑 STEP 3: VERIFY API KEYS (1 min)

Make sure your `.env` has:
```
GEMINI_API_KEY=...
ELEVENLABS_API_KEY=...
OPENAI_API_KEY=...
```

**Test ElevenLabs key:**
Go to: https://elevenlabs.io/
Login → Profile → API Keys

---

## 🚀 STEP 4: RUN IT! (1 min)

```bash
python app.py
```

You should see:
```
🎙️ TrainBot Voice Assistant Starting...
✅ Voice features enabled!
Running on local URL: http://127.0.0.1:7860
```

---

## 🧪 TESTING PLAN

### Test 1: Text Chat (Baseline) - 5 mins
1. Upload a PDF
2. Go to "💬 Text Chat" tab
3. Ask: "What is this document about?"
4. ✅ Should get text answer from Gemini

### Test 2: Voice Input + Voice Output - 10 mins
1. Make sure you uploaded materials first!
2. Go to "🎙️ Voice Chat" tab
3. Click the microphone icon to record
4. Say: "What are the main points in this document?"
5. Click stop recording
6. Click "🎙️ Ask with Voice" button
7. Wait 5-10 seconds
8. ✅ Should see:
   - Your transcribed question
   - Text answer from Gemini
   - Audio player with voice response!

### Test 3: Different Questions - 5 mins
Try these voice questions:
- "Summarize this in simple terms"
- "What are the key takeaways?"
- "Explain the main concept"

---

## 🎤 VOICE CHAT WORKFLOW

```
1. User clicks microphone
   ↓
2. Records question
   ↓
3. Clicks "Ask with Voice"
   ↓
4. Audio → Whisper API → Text
   ↓
5. Text → Gemini → Answer
   ↓
6. Answer → ElevenLabs → Audio
   ↓
7. Both text and audio shown!
```

---

## 📊 TEST DATA YOU NEED

### For Upload Testing:

**PDFs (3-5 files):**
- Product documentation (5-10 pages)
- Training manual (any topic)
- Technical guide
- Company handbook
- Research paper

**PowerPoints (2-3 files):**
- Presentation slides
- Training deck
- Sales pitch
- Company overview

**Videos (1-2 files):**
- Short training video (2-5 mins)
- Product demo recording
- Webinar clip
- Tutorial video

**Where to find test data:**

1. **Your own materials** (if you have any)

2. **Create sample PDFs:**
   - Open Google Docs
   - Write a fake "Product Training Guide"
   - Download as PDF

3. **Sample videos:**
   - Record yourself explaining something (2 mins)
   - Use OBS Studio or QuickTime to record screen
   - Talk about any topic

4. **Download samples:**
   - GitHub: Search "sample pdf training"
   - YouTube: Download short educational video
   - SlideShare: Download sample presentations

---

## 🎯 MINIMUM TEST SET

**Start with these:**
1. ✅ 1 PDF (5-10 pages about any topic)
2. ✅ 1 PowerPoint (10-15 slides)
3. ✅ 1 short video (2-3 minutes) - OPTIONAL for tonight

**You can test everything with just the PDF!**

---

## ⚠️ COMMON ISSUES

### Issue 1: "No module named 'elevenlabs'"
```bash
pip install elevenlabs
```

### Issue 2: Microphone not working
- Check browser permissions
- Allow microphone access
- Try refreshing the page

### Issue 3: Voice response takes long
- Normal! Audio generation takes 5-10 seconds
- Be patient, don't click multiple times

### Issue 4: "API key invalid"
- Check .env file has correct keys
- No quotes around keys
- No extra spaces

### Issue 5: Audio doesn't play
- Check browser audio isn't muted
- Try Chrome (best support)
- Check file was generated (should see audio player)

---

## 💡 QUICK TEST WITHOUT VIDEO

**If you don't want to mess with videos tonight:**

1. Skip video upload for now
2. Test with just PDFs and PPTs
3. Focus on voice chat working
4. Add video testing tomorrow

**Voice features are the priority!**

---

## 🎯 SUCCESS CRITERIA

By end of tonight, you should have:
- ✅ Voice input working (speak → text)
- ✅ Voice output working (text → audio)
- ✅ Full voice Q&A cycle complete
- ✅ Both text and audio responses
- ✅ Tested with at least 1 PDF

**That's HUGE progress!** 🎉

---

## 📝 TESTING CHECKLIST

```
[ ] Installed elevenlabs library
[ ] voice_processor.py in folder
[ ] app.py updated with voice features
[ ] All API keys in .env
[ ] App starts without errors
[ ] Can upload PDF
[ ] Text chat works
[ ] Microphone records
[ ] Voice question transcribed
[ ] Gemini answers question
[ ] Audio response generated
[ ] Audio plays in browser
```

---

## ⏰ TONIGHT'S TIMELINE

**9:00 PM - 9:15 PM:** Setup
- Install libraries
- Download files
- Verify API keys

**9:15 PM - 9:30 PM:** Test text features
- Upload PDF
- Test text chat
- Confirm baseline works

**9:30 PM - 10:00 PM:** Test voice features
- Record voice question
- Test transcription
- Test voice response
- Debug any issues

**10:00 PM - 10:30 PM:** Polish & test
- Try different questions
- Test edge cases
- Take notes on bugs

**10:30 PM:** STOP and REST!
- Save your work
- Backup files
- Sleep! Tomorrow is Day 2

---

## 🎬 DEMO VIDEO PREP

**While testing, note down:**
- Which test files work best
- Best example questions to ask
- Any bugs you find
- Screenshots of working features

**This will help with demo video on Day 3!**

---

## 🚀 READY?

1. Install libraries
2. Download 2 files
3. Run `python app.py`
4. Test voice chat
5. Celebrate! 🎉

**You got this!** 💪

Questions? Issues? Just paste the error and I'll help!

---

**LET'S MAKE THIS VOICE-ENABLED APP HAPPEN!** 🎙️✨
