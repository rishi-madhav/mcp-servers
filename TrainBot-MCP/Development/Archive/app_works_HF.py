"""
TrainBot - AI Training Course Generator
Theme: Elegant Paper (Beige/Academic)
Status: FINAL PRODUCTION (Fixed Variable Names + Layout + Logic)
"""

import gradio as gr
import os
import time
import tempfile
from dotenv import load_dotenv
import google.generativeai as genai
from fpdf import FPDF

# Try YouTube API
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    YT_AVAILABLE = True
except ImportError:
    YT_AVAILABLE = False

# ============================================
# ⚙️ CONFIGURATION
# ============================================

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("⚠️ WARNING: GEMINI_API_KEY not found.")
    MODEL_NAME = "models/gemini-1.5-flash"
else:
    genai.configure(api_key=api_key)
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        priority = [
            "models/gemini-2.5-flash", "models/gemini-2.0-flash", "models/gemini-1.5-pro",
            "models/gemini-pro-latest", "models/gemini-2.0-flash-exp", "models/gemini-1.5-flash"
        ]
        MODEL_NAME = priority[-1]
        for p in priority:
            if p in available:
                MODEL_NAME = p
                break
        print(f"✅ Active Model: {MODEL_NAME}")
    except:
        MODEL_NAME = "models/gemini-1.5-flash"

DOC_STORE = {}

# ============================================
# 🧠 LOGIC
# ============================================

def process_uploaded_file(file_obj):
    if not file_obj: return None, "No file"
    filename = os.path.basename(file_obj.name)
    content = ""
    try:
        ext = filename.lower().split('.')[-1]
        if ext == 'pdf':
            from pypdf import PdfReader
            reader = PdfReader(file_obj.name)
            content = "\n".join([page.extract_text() for page in reader.pages])
        elif ext == 'docx':
            import docx
            doc = docx.Document(file_obj.name)
            content = "\n".join([para.text for para in doc.paragraphs])
        elif ext in ['txt', 'csv', 'md', 'py', 'json']:
            with open(file_obj.name, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        else:
            content = f"[Media/Binary File: {filename}]"
        
        DOC_STORE[filename] = content
        return filename, "Success"
    except Exception as e:
        return filename, f"Error: {str(e)}"

def process_youtube(url):
    if not url: return None, "No URL"
    if "youtube.com" not in url and "youtu.be" not in url: return None, "Invalid URL"
    try:
        vid = url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1]
        filename = f"YT_{vid}"
        text = f"YouTube Video: {url}"
        if YT_AVAILABLE:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(vid)
                text += "\n" + " ".join([t['text'] for t in transcript])
            except: text += " (No Transcript)"
        DOC_STORE[filename] = text
        return filename, "Success"
    except Exception as e: return None, str(e)

def process_voice(audio_path, selected_files):
    if not audio_path: return "Please record audio first."
    if not api_key: return "API Key missing."
    try:
        myfile = genai.upload_file(audio_path)
        while myfile.state.name == "PROCESSING":
            time.sleep(1)
            myfile = genai.get_file(myfile.name)
        context = ""
        if selected_files:
            for fname in selected_files:
                if fname in DOC_STORE:
                    context += f"\nFile: {fname}\n{DOC_STORE[fname][:5000]}\n"
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content([f"Context:\n{context}\n\nTask: Answer audio question.", myfile])
        return response.text
    except Exception as e: return f"Voice Error: {str(e)}"

def process_summary(summary_type, selected_files):
    if not selected_files: return "Please select files first."
    context = ""
    for fname in selected_files:
        if fname in DOC_STORE:
            context += f"\nFile: {fname}\n{DOC_STORE[fname][:10000]}\n"
    if not context: return "Selected files are empty."
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(f"Create a {summary_type} summary of the following material:\n\n{context}")
        return response.text
    except Exception as e: return f"Summary Error: {str(e)}"

def generate_content_core(mode, title, modules, level, f_count, f_level, lang, selected_files):
    context = ""
    if selected_files:
        for fname in selected_files:
            if fname in DOC_STORE:
                context += f"\n--- Source: {fname} ---\n{DOC_STORE[fname][:15000]}\n"
    
    model = genai.GenerativeModel(MODEL_NAME)
    if mode == "Flashcards":
        prompt = f"""Role: Tutor. Task: Create {f_count} flashcards. Topic: {title}. Level: {f_level}. Lang: {lang}. Material: {context}. Output format: Card 1:\nQ: ...\nA: ..."""
    else:
        prompt = f"""Role: Instructional Designer. Task: Create a {level} course on '{title}'. Modules: {modules}. Lang: {lang}. Material: {context}. Output Markdown."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e: return f"Generation Error: {str(e)}"

# ============================================
# 📄 PDF ENGINE
# ============================================

def clean_text_for_pdf(text):
    replacements = {"**": "", "__": "", "##": "", "# ": "", "•": "-", "–": "-", "—": "-", "“": '"', "”": '"', "’": "'"}
    for old, new in replacements.items(): text = text.replace(old, new)
    return text

def generate_pdf_file(content, title="Generated Content"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", "B", 16)
    try: pdf.cell(0, 10, clean_text_for_pdf(title)[:60], ln=True, align="C")
    except: pdf.cell(0, 10, "Document", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 11)
    for line in content.split('\n'):
        clean = clean_text_for_pdf(line).strip()
        if not clean: pdf.ln(2); continue
        prefix = "  - " if line.strip().startswith("-") or line.strip().startswith("*") else ""
        try: pdf.multi_cell(0, 6, (prefix + clean.lstrip("-* ")).encode('latin-1', 'replace').decode('latin-1'))
        except: continue
    filename = f"TrainBot_Export_{int(time.time())}.pdf"
    path = os.path.join(tempfile.gettempdir(), filename)
    pdf.output(path)
    return path

# ============================================
# 🎨 CSS
# ============================================

css_styles = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+Pro:wght@400;600&display=swap');
:root { --bg-app: #F2F0E9; --bg-sidebar: #E6E4DC; --bg-card: #FFFFFF; --text-main: #2C2C2C; --accent: #2A4365; --border-color: #E5E7EB; }
body { zoom: 90%; }
body, .gradio-container { background-color: var(--bg-app) !important; font-family: 'Source Sans Pro', sans-serif !important; color: var(--text-main) !important; margin: 0 !important; }
h1, h2, h3, .sidebar-title { font-family: 'Playfair Display', serif !important; color: var(--text-main) !important; }
.sidebar { background-color: var(--bg-sidebar) !important; border-right: 1px solid #D4D4D4 !important; padding: 30px 20px !important; min-height: 100vh !important; }
.sidebar-title { font-size: 26px !important; color: var(--accent) !important; margin-bottom: 5px !important; }
.sidebar p, .sidebar li { font-size: 16px !important; line-height: 1.6 !important; color: #4a5568 !important; }
.content-card { background-color: var(--bg-card) !important; border: 1px solid #E5E7EB !important; border-radius: 12px !important; padding: 20px !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important; margin-bottom: 12px !important; }
.full-height-card { min-height: 500px !important; height: 100% !important; }
.explore-col { display: flex !important; flex-direction: column !important; gap: 16px !important; }
.gr-form, .gr-box, .gr-group { background-color: transparent !important; border: none !important; box-shadow: none !important; }
textarea, input, select { background-color: #FFFFFF !important; border: 1px solid #D1D5DB !important; border-radius: 6px !important; padding: 10px !important; box-shadow: none !important; }
.action-btn { font-weight: 600 !important; border-radius: 6px !important; height: 100% !important; padding: 12px !important; font-size: 0.9rem !important; width: 100% !important; }
.primary-btn { background-color: var(--accent) !important; color: white !important; border: none !important; }
.secondary-btn { background-color: white !important; border: 1px solid var(--accent) !important; color: var(--accent) !important; }
.file-upload-zone .svelte-116rqfv { display: flex !important; flex-direction: row !important; white-space: nowrap !important; align-items: center; justify-content: center; gap: 5px; }
.kb-container .gr-checkbox-group { display: flex !important; flex-direction: column !important; gap: 8px !important; }
.kb-container label { display: flex !important; align-items: center !important; background: transparent !important; padding: 5px 0 !important; cursor: pointer !important; }
.kb-container input { margin-right: 10px !important; width: 16px !important; height: 16px !important; }
.coming-soon-box { background: rgba(42, 67, 101, 0.05) !important; border: 1px dashed var(--accent) !important; border-radius: 12px !important; padding: 20px !important; margin-top: 20px !important; text-align: center !important; }
#explore-modal { position: fixed !important; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 80% !important; max-width: 800px !important; z-index: 99999 !important; background: white !important; border-radius: 12px !important; box-shadow: 0 20px 60px rgba(0,0,0,0.4) !important; border: 1px solid #ccc !important; padding: 0 !important; }
.status-text { color: #2A4365 !important; font-weight: bold; margin-top: 10px; }
footer { display: none !important; }
"""

# ============================================
# APP LAYOUT
# ============================================

with gr.Blocks(title="TrainBot") as demo:
    gr.HTML(f"<style>{css_styles}</style>")
    
    processing_state = gr.State([False, "none"]) 
    all_files_state = gr.State([]) 
    course_title_state = gr.State("Course_Material") 
    
    # --- MODAL ---
    with gr.Group(visible=False, elem_id="explore-modal") as explore_modal:
        with gr.Column(elem_classes=["content-card"]):
            modal_header = gr.Markdown("### 💡 Result")
            explore_output = gr.Textbox(label="", lines=15, elem_classes=["clean-input"])
            with gr.Row():
                explore_regen_btn = gr.Button("🔄 Regenerate", elem_classes=["secondary-btn action-btn"])
                # THIS WAS THE FIX: RENAMED VARIABLE TO MATCH LOGIC
                explore_pdf_file = gr.File(label="Download PDF", interactive=False, height=50)
                explore_close_btn = gr.Button("Close", elem_classes=["primary-btn action-btn"])

    with gr.Row(elem_classes=["main-row"]):
        
        # --- SIDEBAR ---
        with gr.Column(scale=0, min_width=300, elem_classes=["sidebar"]):
            if os.path.exists("logo.png"): gr.Image("logo.png", height=80, show_label=False, interactive=False)
            else: gr.Image("https://cdn-icons-png.flaticon.com/512/4762/4762311.png", height=80, show_label=False, interactive=False)
            
            gr.Markdown("# 🎓 TrainBot")
            gr.Markdown("*AI Course Generator*", elem_classes=["sidebar-subtitle"])
            gr.Markdown("---")
            gr.Markdown("### 📖 Guide")
            gr.Markdown("**1. Upload:** Add docs & media.\n**2. Select:** Check files in 'KB'.\n**3. Create:** Use 'Explore' or 'Generate'.")
            gr.Markdown("### ✨ Tips")
            gr.Markdown("* Use clear audio.\n* Verify AI outputs.")
            gr.Markdown("---")
            gr.Markdown("### 🛠️ Credits")
            gr.Markdown("Powered by **Google Gemini**")

        # --- MAIN ---
        with gr.Column(elem_classes=["main-content"]):
            gr.Markdown("# Dashboard")
            
            with gr.Tabs():
                
                # TAB 1: UPLOAD
                with gr.Tab("📂 Upload"):
                    with gr.Row():
                        with gr.Column(elem_classes=["content-card"]):
                            gr.Markdown("### 1. Documents")
                            doc_input = gr.File(label="", file_count="multiple", file_types=[".pdf", ".docx", ".txt"], type="filepath", height=80, elem_classes=["file-upload-zone"])
                        with gr.Column(elem_classes=["content-card"]):
                            gr.Markdown("### 2. Recordings")
                            media_input = gr.File(label="", file_count="multiple", file_types=[".mp3", ".mp4", ".wav"], type="filepath", height=80, elem_classes=["file-upload-zone"])
                        with gr.Column(elem_classes=["content-card"]):
                            gr.Markdown("### 3. YouTube")
                            with gr.Row():
                                yt_input = gr.Textbox(placeholder="Paste URL...", show_label=False, scale=3, container=False, elem_classes=["clean-input"])
                                yt_btn = gr.Button("Add", scale=1, elem_classes=["primary-btn action-btn"])

                    with gr.Column(elem_classes=["content-card", "full-height-card"]):
                        gr.Markdown("### 🗂️ Active Knowledge Base")
                        source_count = gr.Markdown("No files loaded", elem_classes=["status-text"])
                        file_selector = gr.CheckboxGroup(choices=[], label="", value=[], interactive=True, elem_classes=["kb-container"])

                # TAB 2: EXPLORE
                with gr.Tab("🧭 Explore"):
                    with gr.Row():
                        with gr.Column(scale=6, elem_classes=["content-card"]):
                            gr.Markdown("### 💬 Chat with Documents")
                            chatbot = gr.Chatbot(height=500, show_label=False)
                            with gr.Row():
                                chat_input = gr.Textbox(placeholder="Ask a question...", show_label=False, scale=5, container=False, elem_classes=["clean-input"])
                                chat_btn = gr.Button("Send", scale=1, elem_classes=["primary-btn action-btn"])
                            chat_pdf_file = gr.File(label="Export Chat", interactive=False, height=50)
                            chat_export_btn = gr.Button("📥 Export Chat PDF", elem_classes=["secondary-btn small-btn"])

                        with gr.Column(scale=4, elem_classes=["explore-col"]):
                            with gr.Column(elem_classes=["content-card"]):
                                gr.Markdown("### 🎙️ Voice Analyzer")
                                audio_input = gr.Audio(sources=["microphone"], type="filepath", label="")
                                voice_btn = gr.Button("🎤 Analyze Audio", elem_classes=["secondary-btn action-btn"])
                                voice_status = gr.Markdown("", elem_classes=["status-text"])
                            
                            with gr.Column(elem_classes=["content-card"]):
                                gr.Markdown("### 📝 Content Summarizer")
                                summary_type = gr.Dropdown(["Executive", "Detailed", "Key Points"], value="Executive", label="Type", elem_classes=["clean-dropdown"])
                                summary_btn = gr.Button("📄 Summarize", elem_classes=["secondary-btn action-btn"])
                                summary_status = gr.Markdown("", elem_classes=["status-text"])

                # TAB 3: GENERATE
                with gr.Tab("✨ Generate"):
                    with gr.Row():
                        with gr.Column(scale=4, elem_classes=["content-card"]):
                            gr.Markdown("### Configuration")
                            content_type = gr.Dropdown(["Full Course", "Micro Course", "Flashcards", "Quiz"], value="Full Course", label="Content Type", elem_classes=["clean-dropdown"])
                            
                            with gr.Group(visible=True) as group_course:
                                gen_title = gr.Textbox(label="Title", value="My New Course", elem_classes=["clean-input"])
                                with gr.Row():
                                    course_modules = gr.Dropdown([3, 4, 5, 6, 8, 10], value=5, label="Modules", elem_classes=["clean-dropdown"])
                                    course_level = gr.Dropdown(["Beginner", "Intermediate", "Advanced"], value="Intermediate", label="Level", elem_classes=["clean-dropdown"])
                            
                            with gr.Group(visible=False) as group_micro:
                                micro_style = gr.Dropdown(["Short Concepts", "Executive Overview", "Technical Bytes"], value="Short Concepts", label="Style", elem_classes=["clean-dropdown"])

                            with gr.Group(visible=False) as group_quiz:
                                quiz_q = gr.Number(value=5, minimum=1, maximum=10, label="Questions", elem_classes=["clean-input"])

                            with gr.Group(visible=False) as group_flash:
                                with gr.Row():
                                    flash_count = gr.Dropdown([5, 10, 15, 20], value=10, label="Count", elem_classes=["clean-dropdown"])
                                    flash_level = gr.Dropdown(["Basic", "Intermediate", "Advanced"], value="Intermediate", label="Difficulty", elem_classes=["clean-dropdown"])
                                
                            gen_language = gr.Dropdown(["English", "Spanish", "French"], value="English", label="Language", elem_classes=["clean-dropdown"])

                        with gr.Column(scale=6, elem_classes=["content-card"]):
                            gr.Markdown("### Output Preview")
                            gen_output = gr.Textbox(label="", lines=26, elem_classes=["clean-input"], placeholder="Generated content will appear here...")
                            
                            gr.Markdown("### Actions")
                            with gr.Row():
                                generate_btn = gr.Button("🚀 Generate", scale=1, elem_classes=["primary-btn action-btn"])
                                regenerate_btn = gr.Button("🔄 Regenerate", scale=1, elem_classes=["secondary-btn action-btn"])
                                modal_pdf_file = gr.File(label="Export PDF", interactive=False, height=50)

                    with gr.Row(elem_classes=["coming-soon-box"]):
                        gr.Markdown("### 🚀 Coming Soon:  SCORM Export  |  AI Video Avatars  |  Enterprise LMS API")

    # ══════════════════════════════════════════════════
    # LOGIC WIRING
    # ══════════════════════════════════════════════════

    def handle_upload(files, all_files, current_selection):
        if files is None: return gr.update(), gr.update(), all_files, None
        for file in files:
            filename, msg = process_uploaded_file(file)
            if filename and "Error" not in msg:
                if filename not in all_files: all_files.append(filename)
                if current_selection is None: current_selection = []
                if filename not in current_selection: current_selection.append(filename)
        return gr.CheckboxGroup(choices=all_files, value=current_selection), f"**Total Files: {len(all_files)}**", all_files, None

    doc_input.change(handle_upload, [doc_input, all_files_state, file_selector], [file_selector, source_count, all_files_state, doc_input])
    media_input.change(handle_upload, [media_input, all_files_state, file_selector], [file_selector, source_count, all_files_state, media_input])
    
    def handle_yt(url, all_files, current_selection):
        if not url: return gr.update(), gr.update(), all_files, ""
        fname = f"YouTube_Link_{len(all_files)+1}"
        DOC_STORE[fname] = f"Content from YouTube: {url}"
        all_files.append(fname)
        current_selection = all_files if current_selection is None else current_selection + [fname]
        return gr.CheckboxGroup(choices=all_files, value=current_selection), f"**Total Files: {len(all_files)}**", all_files, ""
    
    yt_btn.click(handle_yt, [yt_input, all_files_state, file_selector], [file_selector, source_count, all_files_state, yt_input])

    def chat_logic(msg, hist, files):
        if not msg: return hist, ""
        context = ""
        if files:
            for f in files:
                if f in DOC_STORE: context += DOC_STORE[f][:2000] + "\n"
        if not api_key: return hist + [[msg, "Please set API Key"]], ""
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            resp = model.generate_content(f"Context: {context}\n\nQuestion: {msg}")
            return hist + [[msg, resp.text]], ""
        except Exception as e: return hist + [[msg, str(e)]], ""

    chat_btn.click(chat_logic, [chat_input, chatbot, file_selector], [chatbot, chat_input], show_progress="hidden")
    chat_input.submit(chat_logic, [chat_input, chatbot, file_selector], [chatbot, chat_input], show_progress="hidden")
    
    def export_chat(history):
        if not history: return None
        text = "\n\n".join([f"Q: {h[0]}\n\nA: {h[1]}" for h in history])
        return generate_pdf_file(text, "Chat History")
    chat_export_btn.click(export_chat, [chatbot], [chat_pdf_file])

    def trigger_voice(audio, files, proc_state, progress=gr.Progress()):
        if proc_state[0]: return gr.update(), "⚠️ Locked", "none", proc_state, gr.update(), gr.update()
        new_state = [True, "voice"]
        try:
            progress(0.1, desc="Analyzing...")
            res = process_voice(audio, files)
            header = "### 🎙️ Voice Analysis Output"
            visible = True
        except Exception as e: res = str(e); header="Error"; visible=True
        progress(1.0, desc="Done")
        # FIXED: Added explore_pdf_file to outputs
        pdf_path = generate_pdf_file(res, "Voice Analysis")
        return gr.update(visible=visible), res, header, [False, "voice"], gr.update(value=""), gr.update(value=""), gr.update(value=pdf_path, visible=True)

    def trigger_summary(sType, files, proc_state, progress=gr.Progress()):
        if proc_state[0]: return gr.update(), "⚠️ Locked", "none", proc_state, gr.update(), gr.update()
        new_state = [True, "summary"]
        try:
            progress(0.1, desc="Summarizing...")
            res = process_summary(sType, files)
            header = "### 📄 Document Summary Output"
            visible = True
        except Exception as e: res = str(e); header="Error"; visible=True
        progress(1.0, desc="Done")
        # FIXED: Added explore_pdf_file to outputs
        pdf_path = generate_pdf_file(res, "Summary")
        return gr.update(visible=visible), res, header, [False, "summary"], gr.update(value=""), gr.update(value=""), gr.update(value=pdf_path, visible=True)

    def set_loading_voice(): return "⏳ Analyzing...", gr.update(interactive=False)
    def set_loading_summary(): return "⏳ Summarizing...", gr.update(interactive=False)
    def unlock(): return "", gr.update(interactive=True)

    voice_btn.click(set_loading_voice, None, [voice_status, summary_btn]).then(
        trigger_voice, [audio_input, file_selector, processing_state], 
        [explore_modal, explore_output, modal_header, processing_state, voice_status, summary_btn, explore_pdf_file]
    ).then(unlock, None, [voice_status, summary_btn])

    summary_btn.click(set_loading_summary, None, [summary_status, voice_btn]).then(
        trigger_summary, [summary_type, file_selector, processing_state], 
        [explore_modal, explore_output, modal_header, processing_state, summary_status, voice_btn, explore_pdf_file]
    ).then(unlock, None, [summary_status, voice_btn])

    def trigger_regen_explore(proc_state, audio, sType, files):
        _, mode = proc_state
        if mode == "voice": return process_voice(audio, files)
        if mode == "summary": return process_summary(sType, files)
        return "Nothing to regenerate"

    explore_regen_btn.click(trigger_regen_explore, [processing_state, audio_input, summary_type, file_selector], [explore_output])
    explore_close_btn.click(lambda: gr.update(visible=False), None, explore_modal)

    def trigger_generation_fixed(mode, title, mod, lvl, m_style, qq, fq, fl, lang, files, saved_title, progress=gr.Progress()):
        progress(0.1, desc="Starting...")
        actual_title = title if mode == "Full Course" and title else saved_title
        if not actual_title: actual_title = "Course_Material"
        res = generate_content_core(mode, actual_title, mod, lvl, fq, fl, lang, files)
        progress(0.9, desc="Creating PDF...")
        pdf = generate_pdf_file(res, actual_title)
        progress(1.0, desc="Done")
        return res, pdf, actual_title

    for btn in [generate_btn, regenerate_btn]:
        btn.click(
            trigger_generation_fixed, 
            [content_type, gen_title, course_modules, course_level, micro_style, quiz_q, flash_count, flash_level, gen_language, file_selector, course_title_state], 
            [gen_output, modal_pdf_file, course_title_state]
        )

    def toggle_inputs(c_type):
        if c_type == "Flashcards": return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)
        if c_type == "Micro Course": return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
        if c_type == "Quiz": return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)
        return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
    
    content_type.change(toggle_inputs, [content_type], [group_course, group_micro, group_quiz, group_flash])

if __name__ == "__main__":
    demo.launch()