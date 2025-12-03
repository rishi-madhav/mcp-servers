# 🧪 Testing Guide for StudyBuddy

## Pre-Flight Checklist

Before testing, ensure:
- [ ] `.env` file has valid `GEMINI_API_KEY`
- [ ] Virtual environment is activated
- [ ] Dependencies are installed (`./setup.sh` completed)
- [ ] Database is initialized (auto-created on first run)

## Testing Sequence

### 1. Test Database Initialization

```bash
python -c "
import asyncio
from mcp_server import database as db
async def test():
    await db.init_database()
    student_id = await db.get_or_create_student('Test Student', 8, 'CBSE')
    print(f'✅ Student created with ID: {student_id}')
asyncio.run(test())
"
```

**Expected**: Student ID printed, no errors

### 2. Test Gemini Client

```bash
python -c "
import asyncio
from mcp_server.gemini_client import get_gemini_client

async def test():
    client = get_gemini_client()
    result = await client.generate_content(
        'Return this JSON: {\"test\": \"success\", \"message\": \"Gemini is working!\"}'
    )
    print(result)

asyncio.run(test())
"
```

**Expected**: JSON response with success message

### 3. Test MCP Server with Inspector

```bash
# Install MCP Inspector (if not already installed)
npm install -g @modelcontextprotocol/inspector

# Run inspector
npx @modelcontextprotocol/inspector python -m mcp_server.server
```

**Expected**:
- Inspector UI opens in browser
- 5 tools visible: studybuddy_explain_topic, studybuddy_generate_practice, etc.
- Can execute tools and see JSON responses

**Test Cases in Inspector**:

**Tool 1: studybuddy_explain_topic**
```json
{
  "topic": "Photosynthesis",
  "subject": "Science",
  "grade": 8,
  "board": "CBSE"
}
```

**Tool 2: studybuddy_generate_practice**
```json
{
  "topic": "Fractions",
  "subject": "Mathematics",
  "grade": 6,
  "board": "CBSE",
  "num_questions": 3
}
```

**Tool 3: studybuddy_solve_step_by_step**
```json
{
  "problem": "Solve: 2x + 5 = 15",
  "subject": "Mathematics",
  "grade": 7
}
```

**Tool 4: studybuddy_create_story**
```json
{
  "topic": "Water Cycle",
  "subject": "Science",
  "grade": 5
}
```

**Tool 5: studybuddy_quiz_me**
```json
{
  "topic": "Cell Division",
  "subject": "Biology",
  "grade": 9,
  "board": "ICSE"
}
```

### 4. Test Gradio App

```bash
python gradio_app/app.py
```

**Manual Test Flow**:

1. **Profile Setup**:
   - Enter name: "Test Student"
   - Grade: 8
   - Board: CBSE
   - Click "Setup Profile"
   - ✅ Should see: "Welcome, Test Student! (Grade 8, CBSE)"

2. **Explain Topic Tab**:
   - Topic: "Photosynthesis"
   - Subject: "Science"
   - Click "Explain"
   - ✅ Should see JSON with explanation, key_points, real_world_example

3. **Practice Problems Tab**:
   - Topic: "Quadratic Equations"
   - Subject: "Mathematics"
   - Number: 5
   - Click "Generate Problems"
   - ✅ Should see JSON with 5 problems array

4. **Solve Problem Tab**:
   - Problem: "If 3x - 7 = 20, find x"
   - Subject: "Mathematics"
   - Click "Solve"
   - ✅ Should see JSON with steps array and final_answer

5. **Story Mode Tab**:
   - Topic: "Gravity"
   - Subject: "Science"
   - Click "Create Story"
   - ✅ Should see JSON with story_title, story, characters

6. **Quiz Me Tab**:
   - Topic: "Digestive System"
   - Subject: "Biology"
   - Click "Start Quiz"
   - ✅ Should see JSON with 10 questions
   - Run again with same inputs
   - ✅ Questions should be different (no repeats)

7. **My Progress Tab**:
   - Click "Load History"
   - ✅ Should see explained_topics, practice_problems, quiz_results

### 5. Test Claude Desktop Integration

1. **Update Claude Desktop config**:
```bash
# Mac
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Add:
{
  "mcpServers": {
    "studybuddy": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "env": {
        "PYTHONPATH": "/path/to/studybuddy-mcp",
        "GEMINI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

2. **Restart Claude Desktop**

3. **Test in Claude**:
   - Ask: "Use studybuddy to explain photosynthesis for grade 8"
   - ✅ Should use MCP tool and return structured explanation

### 6. Load Testing

**Test Concurrent Requests**:

```python
import asyncio
import aiohttp

async def test_load():
    tasks = []
    for i in range(10):
        task = asyncio.create_task(
            # Your API call here
        )
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    print(f"Completed {len(results)} requests")

asyncio.run(test_load())
```

## Common Issues & Solutions

### Issue: "GEMINI_API_KEY not found"
**Solution**: Check `.env` file exists and has the key

### Issue: "Database locked"
**Solution**: Close other connections, restart app

### Issue: "Module not found"
**Solution**: Ensure virtual environment is activated, run `uv pip install -e .`

### Issue: JSON parsing errors
**Solution**: Gemini sometimes adds extra text. The `_clean_json_response` function handles this, but check prompt clarity

### Issue: MCP Inspector can't find server
**Solution**: 
```bash
# Make sure you're in the project directory
cd /path/to/studybuddy-mcp
# Activate venv
source .venv/bin/activate
# Run inspector with full path
npx @modelcontextprotocol/inspector python -m mcp_server.server
```

## Performance Benchmarks

**Expected Response Times**:
- Explain Topic: 2-4 seconds
- Generate Practice: 3-5 seconds
- Solve Problem: 2-4 seconds
- Create Story: 4-6 seconds
- Quiz Me: 5-8 seconds (longer due to duplicate checking)

## Quality Checklist

Before submitting:
- [ ] All 5 MCP tools work correctly
- [ ] Gradio UI loads without errors
- [ ] Database persists data correctly
- [ ] Quiz avoids duplicate questions
- [ ] JSON responses are valid and structured
- [ ] Error messages are actionable
- [ ] Profile setup works
- [ ] History tracking works
- [ ] UI is responsive and professional
- [ ] All buttons have hover effects
- [ ] Dark mode looks good

## Demo Recording Checklist

Record a 3-5 minute video showing:
1. ✅ Quick intro (10 seconds)
2. ✅ Profile setup (15 seconds)
3. ✅ Explain topic feature (30 seconds)
4. ✅ Generate practice (30 seconds)
5. ✅ Story mode (30 seconds)
6. ✅ Quiz feature with duplicate avoidance (60 seconds)
7. ✅ History view (20 seconds)
8. ✅ MCP integration in Claude Desktop (45 seconds)
9. ✅ Closing + sponsor mentions (20 seconds)

**Tools for recording**:
- Mac: QuickTime Screen Recording
- Windows: OBS Studio
- Web: Loom

**Editing tips**:
- Add captions for key features
- Speed up slow parts (2x)
- Add background music (low volume)
- Keep under 5 minutes!
