# ⚡ Quick Start Reference

## 30-Second Setup

```bash
# 1. Get Gemini API key
open https://makersuite.google.com/app/apikey

# 2. Setup
./setup.sh

# 3. Add API key to .env
echo "GEMINI_API_KEY=your_key_here" > .env

# 4. Run app
source .venv/bin/activate
python gradio_app/app.py
```

Open http://localhost:7860 ✅

---

## File Structure

```
studybuddy-mcp/
├── mcp_server/
│   ├── server.py          # 5 MCP tools
│   ├── database.py        # SQLite ops
│   ├── prompts.py         # Gemini prompts
│   └── gemini_client.py   # API client
├── gradio_app/
│   └── app.py            # UI
├── data/
│   └── studybuddy.db     # Auto-created
└── .env                  # ADD YOUR KEY HERE!
```

---

## Testing One-Liner

```bash
# Test everything
python -c "import asyncio; from mcp_server.database import init_database; asyncio.run(init_database()); print('✅ DB OK')" && \
python -c "from mcp_server.gemini_client import get_gemini_client; print('✅ Gemini OK')" && \
echo "✅ All systems go!"
```

---

## Common Commands

```bash
# Activate venv
source .venv/bin/activate

# Run Gradio app
python gradio_app/app.py

# Test MCP with Inspector
npx @modelcontextprotocol/inspector python -m mcp_server.server

# Deploy to Modal
modal deploy modal_deploy.py
```

---

## Claude Desktop Config

**Location**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "studybuddy": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "env": {
        "PYTHONPATH": "/FULL/PATH/TO/studybuddy-mcp",
        "GEMINI_API_KEY": "your_api_key"
      }
    }
  }
}
```

Restart Claude Desktop after editing.

---

## 5 MCP Tools

1. **studybuddy_explain_topic**
   - Args: topic, subject, grade, board
   - Returns: Explanation with key points

2. **studybuddy_generate_practice**
   - Args: topic, subject, grade, board, num_questions
   - Returns: Practice problems array

3. **studybuddy_solve_step_by_step**
   - Args: problem, subject, grade
   - Returns: Step-by-step solution

4. **studybuddy_create_story**
   - Args: topic, subject, grade
   - Returns: Engaging story

5. **studybuddy_quiz_me**
   - Args: topic, subject, grade, board
   - Returns: 10 quiz questions (no repeats!)

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Import errors | `source .venv/bin/activate` |
| Gemini API error | Check `.env` has valid key |
| Database locked | Restart app |
| MCP not found | Check Claude Desktop config path |
| Port 7860 in use | Change port in `app.py` |

---

## Priority Checklist

**Before testing**:
- [ ] Gemini API key in `.env`
- [ ] Dependencies installed
- [ ] Virtual env activated

**Before submitting**:
- [ ] All 5 tools tested
- [ ] Gradio UI polished
- [ ] Demo video recorded
- [ ] Social post created
- [ ] HF Space published

---

## Sponsor Integration Proof

**For README/Demo**:
- ✅ "Powered by Google Gemini 1.5 Flash"
- ✅ "Deployed on Modal for serverless scaling"
- 📸 Show Gemini logo in UI
- 📸 Show Modal deployment dashboard
- 📝 Mention cost efficiency and speed

---

## Demo Video Script (3 min)

```
0:00 - Hi! This is StudyBuddy for Indian students
0:10 - Setup profile (grade 8, CBSE)
0:25 - Explain photosynthesis
0:55 - Generate practice problems
1:25 - Fun story mode
1:55 - Quiz with smart question tracking
2:40 - View progress history
3:00 - Built with MCP + Gemini, thank sponsors!
```

---

## Key Files to Focus On

**If short on time, prioritize**:
1. `gradio_app/app.py` - UI polish (YOUR STRENGTH)
2. `README.md` - Clear documentation
3. Demo video - Showcase features
4. `mcp_server/server.py` - Ensure tools work

Skip if needed:
- ElevenLabs integration
- Advanced export features
- Extra CSS animations

---

## Success Criteria

**Minimum** (must have):
- ✅ 5 working MCP tools
- ✅ Functional Gradio UI
- ✅ Database persistence
- ✅ Deployed somewhere
- ✅ Basic documentation

**Target** (for prizes):
- ✅ All above PLUS
- ✅ Polished UI
- ✅ Great demo video
- ✅ Strong sponsor mentions
- ✅ Social engagement

---

## Time Allocation

| Phase | Time | Focus |
|-------|------|-------|
| Setup & Test | 2h | Get it working |
| UI Polish | 3h | Make it beautiful |
| Deploy | 1h | Get it live |
| Demo & Docs | 1h | Show it off |
| Buffer | 30m | Fix issues |

**Total: 6.5 hours** ⏰

---

## Remember

- 🎯 Focus on what makes you stand out (UI/UX)
- 🚀 Ship something working > perfect but incomplete
- 💎 Polish = competitive advantage
- 📣 Tell the story in demo video
- 🏆 Target Gemini + Modal awards specifically

**You've got this! 🔥**
