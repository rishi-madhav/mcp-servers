# 🧪 TRAINBOT TESTING CHECKLIST
## Friday, November 28 - Production Readiness Testing

---

## **📋 TEST SUITE (60 minutes)**

### **TEST 1: File Upload (15 mins)**

**PDF Upload:**
- [ ] Upload small PDF (2-3 pages) - works?
- [ ] Upload large PDF (20+ pages) - works?
- [ ] Upload PDF with images - works?
- [ ] Upload corrupted PDF - shows error?
- [ ] Check file size displayed correctly
- [ ] Check character count makes sense

**PowerPoint Upload:**
- [ ] Upload PPTX - works?
- [ ] Upload PPT (old format) - works?
- [ ] Check slides counted correctly
- [ ] Check text extraction works

**Word Document Upload:**
- [ ] Upload DOCX - works?
- [ ] Upload DOC (old format) - works?
- [ ] Check content extraction

**Video Upload:**
- [ ] Upload short MP4 (2-5 min) - works?
- [ ] Check transcription with Gemini
- [ ] Verify duration shown correctly
- [ ] Note: May take 2-5 mins to process

**Edge Cases:**
- [ ] Upload without selecting file - error message clear?
- [ ] Upload unsupported file type - error message clear?
- [ ] Upload multiple files in sequence - all stored?
- [ ] Check total count updates correctly

---

### **TEST 2: Text Chat (15 mins)**

**Before Upload:**
- [ ] Try to chat without uploading - shows friendly message?

**After Upload:**
- [ ] Ask simple question - gets answer?
- [ ] Ask complex question - gets detailed answer?
- [ ] Ask irrelevant question - handles gracefully?
- [ ] Multiple questions in conversation - context maintained?

**Test Questions:**
```
1. "What is this document about?"
2. "Summarize the key points"
3. "What are the main features?"
4. "Explain [specific term from document]"
5. "Compare [concept A] and [concept B]"
```

**Check:**
- [ ] Response time < 5 seconds
- [ ] Answers are relevant
- [ ] Formatting is readable
- [ ] Citations/sources mentioned if applicable

---

### **TEST 3: Voice Chat (15 mins)**

**Before Upload:**
- [ ] Try voice chat without materials - shows message?

**After Upload:**
- [ ] Click microphone - browser asks permission?
- [ ] Record 5-second question - recording works?
- [ ] Click "Ask" - shows processing?
- [ ] Wait for response - transcription shows?
- [ ] Audio plays - voice quality good?
- [ ] Text answer also shows - readable?

**Test with:**
```
1. Short question (5 sec): "What is this about?"
2. Medium question (10 sec): "Can you summarize the main points?"
3. Clear speech - works well?
4. Fast speech - still transcribes?
```

**Check:**
- [ ] Transcription accuracy good?
- [ ] Voice sounds natural (ElevenLabs)
- [ ] Audio plays automatically or has play button?
- [ ] Total time < 15 seconds from question to answer

---

### **TEST 4: Course Generation (10 mins)**

**Full Course:**
- [ ] Generate with default settings - works?
- [ ] Change to Beginner level - content appropriate?
- [ ] Change to Advanced level - content appropriate?
- [ ] Try 3 modules - generates quickly?
- [ ] Try 10 modules - still works?
- [ ] Different topic - generates relevant content?

**Check Output:**
- [ ] Has clear structure (title, modules, objectives)
- [ ] Module count matches slider
- [ ] Skill level reflected in content depth
- [ ] Markdown formatting displays correctly
- [ ] No truncated/cut-off text

**Micro-Course:**
- [ ] Click Micro-Course tab
- [ ] Generate with default topic - works?
- [ ] Content is more concise than full course?
- [ ] Still has useful structure?

---

### **TEST 5: UI/UX (5 mins)**

**Visual:**
- [ ] All three cards visible side-by-side? (desktop)
- [ ] Cards have proper shadows?
- [ ] No scrolling needed on main page? (desktop)
- [ ] Text is readable (font size, contrast)
- [ ] Buttons look clickable

**Interaction:**
- [ ] Buttons respond to hover?
- [ ] Tabs switch smoothly?
- [ ] Loading states show when processing?
- [ ] Error messages are friendly and clear?

**Mobile/Tablet (if you can test):**
- [ ] Cards stack vertically?
- [ ] Everything still accessible?
- [ ] Buttons are tap-able?

---

### **TEST 6: Error Handling (5 mins)**

**Try to break it:**
- [ ] Submit empty forms - handled?
- [ ] Very long questions - handled?
- [ ] Special characters in input - handled?
- [ ] Rapid clicking buttons - no crashes?
- [ ] Close/reload during processing - recovers?

**Check error messages:**
- [ ] Are they user-friendly?
- [ ] Do they explain what to do next?
- [ ] No technical jargon/stack traces shown?

---

## **🐛 BUG TRACKING**

As you test, note any issues here:

### **Critical Bugs (Must Fix Today):**
```
1. 
2. 
3. 
```

### **Minor Issues (Fix if Time):**
```
1. 
2. 
3. 
```

### **Nice-to-Have Improvements:**
```
1. 
2. 
3. 
```

---

## **✅ SIGN-OFF CHECKLIST**

After all tests:
- [ ] No critical bugs found
- [ ] All major features work
- [ ] Error messages are clear
- [ ] App feels responsive
- [ ] Ready for demo video recording

**If you found critical bugs:** Fix them in Hour 2
**If everything works:** Move to Hour 2 (production improvements)

---

## **📝 NOTES:**

*Use this space to jot down observations:*

```
Test results:
-
-
-

Issues found:
-
-
-

Performance notes:
-
-
-
```

---

**Time to start testing: 12:00 PM IST**
**Target completion: 1:00 PM IST**

Good luck! 🧪✨
