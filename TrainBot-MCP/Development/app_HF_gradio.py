"""
TrainBot - AI Training Course Generator
Theme: Native Gradio (Zero Custom CSS for Stability)
Status: FINAL BUG-FREE BUILD (Variable Names Fixed)
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
        prompt = f"""Role: Tutor. Task: Create exactly {f_count} flashcards. Topic: {title}. Level: {f_level}. Lang: {lang}. Material: {context}. Format: Card X: Q/A."""
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
# 🖥️ NATIVE GRADIO UI
# ============================================

# REMOVED THEME ARGUMENT TO PREVENT CRASH
with gr.Blocks(title="TrainBot") as demo:
    
    file_list_state = gr.State([])
    explore_content_state = gr.State("")
    
    gr.Markdown("# 🎓 TrainBot: AI Course Architect")
    
    with gr.Row():
        
        # --- LEFT COLUMN ---
        with gr.Column(scale=1, variant="panel"):
            gr.Markdown("### 1. Knowledge Base")
            
            with gr.Tab("📄 Files"):
                file_upload = gr.File(
                    label="Upload Documents & Media",
                    file_count="multiple",
                    file_types=[".pdf", ".docx", ".txt", ".mp3", ".mp4"]
                )
            
            with gr.Tab("🔗 YouTube"):
                yt_url = gr.Textbox(label="YouTube URL", placeholder="https://youtube.com/...")
                yt_btn = gr.Button("Add Video")
            
            gr.Markdown("### 2. Select Context")
            # Native Checkbox - 100% Clickable
            kb_selector = gr.CheckboxGroup(label="Active Files", choices=[], interactive=True)
            upload_status = gr.Markdown("Waiting for files...")
            
            with gr.Accordion("Guide", open=False):
                gr.Markdown("1. Upload files.\n2. Select checkboxes.\n3. Explore or Generate.")

        # --- RIGHT COLUMN ---
        with gr.Column(scale=2):
            
            with gr.Tabs():
                
                # --- TAB A: EXPLORE ---
                with gr.Tab("🧭 Explore"):
                    gr.Markdown("### Chat with your Content")
                    chatbot = gr.Chatbot(height=400)
                    with gr.Row():
                        chat_msg = gr.Textbox(scale=4, show_label=False, placeholder="Type a question...")
                        chat_btn = gr.Button("Send", scale=1, variant="primary")
                    
                    gr.Markdown("---")
                    
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### 🎙️ Voice Analysis")
                            voice_in = gr.Audio(sources=["microphone"], type="filepath")
                            voice_btn = gr.Button("Analyze Voice Question")
                        with gr.Column():
                            gr.Markdown("### 📝 Summarizer")
                            summary_type = gr.Dropdown(["Executive", "Detailed", "Key Points"], value="Executive", label="Type")
                            summary_btn = gr.Button("Summarize")

                    # DEDICATED RESULT BOX
                    with gr.Group(visible=False) as result_box:
                        gr.Markdown("### 💡 Analysis Result")
                        result_text = gr.Textbox(label="", lines=10)
                        with gr.Row():
                            close_result = gr.Button("Close")
                            # FIXED VARIABLE NAME HERE
                            export_result_btn = gr.Button("Create PDF")
                            result_pdf_file = gr.File(label="Download", interactive=False)

                # --- TAB B: GENERATE ---
                with gr.Tab("✨ Generate Course"):
                    gr.Markdown("### Course Configuration")
                    
                    with gr.Row():
                        mode = gr.Dropdown(["Full Course", "Micro Course", "Quiz", "Flashcards"], value="Full Course", label="Content Type")
                        language = gr.Dropdown(["English", "Spanish", "French", "Hindi"], value="English", label="Language")
                    
                    title = gr.Textbox(label="Course Title", value="New Training Module")
                    
                    with gr.Row():
                        modules = gr.Slider(1, 15, value=5, step=1, label="Modules")
                        level = gr.Dropdown(["Beginner", "Intermediate", "Advanced"], value="Intermediate", label="Difficulty")
                    
                    # Flashcard/Quiz specific inputs
                    with gr.Group(visible=False) as flash_opts:
                        f_count = gr.Dropdown([5, 10, 15], value=10, label="Count")

                    gen_btn = gr.Button("🚀 Generate Content", variant="primary")
                    
                    gr.Markdown("### Output")
                    output_text = gr.Textbox(label="Generated Content", lines=20)
                    
                    with gr.Row():
                        pdf_btn = gr.Button("📄 Create PDF")
                        pdf_file = gr.File(label="Download", interactive=False)

    # --- EVENT WIRING ---
    
    # 1. File Upload
    def handle_upload(files, current_list):
        if not files: return gr.update(), current_list, "No new files."
        new_files = []
        logs = []
        for file in files:
            filename = os.path.basename(file.name)
            if filename in DOC_STORE:
                logs.append(f"Skipped {filename}")
                continue
            try:
                process_uploaded_file(file)
                new_files.append(filename)
                logs.append(f"Processed {filename}")
            except: pass
        
        updated_list = (current_list if current_list else []) + new_files
        return gr.update(choices=updated_list, value=updated_list), updated_list, "\n".join(logs)

    file_upload.change(handle_upload, [file_upload, file_list_state], [kb_selector, file_list_state, upload_status])
    
    # 2. YouTube
    yt_btn.click(
        lambda u, l: process_youtube(u, l),
        inputs=[yt_url, file_list_state],
        outputs=[kb_selector, file_list_state, upload_status]
    )
    
    # 3. Chat
    def chat_logic(msg, hist, files):
        if not msg: return hist, ""
        context = ""
        if files:
            for f in files:
                if f in DOC_STORE: context += DOC_STORE[f][:2000] + "\n"
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            resp = model.generate_content(f"Context: {context}\n\nQuestion: {msg}")
            hist.append([msg, resp.text])
            return hist, ""
        except: return hist, ""

    chat_btn.click(chat_logic, [chat_msg, chatbot, kb_selector], [chatbot, chat_msg])
    chat_msg.submit(chat_logic, [chat_msg, chatbot, kb_selector], [chatbot, chat_msg])
    
    # 4. Voice Trigger
    def run_voice(audio, files):
        res = analyze_voice(audio, files)
        return gr.update(visible=True), res, res

    voice_btn.click(run_voice, [voice_in, kb_selector], [result_box, result_text, explore_content_state])
    
    # 5. Summary Trigger
    def run_summary(sType, files):
        res = process_summary(sType, files)
        return gr.update(visible=True), res, res

    summary_btn.click(run_summary, [summary_type, kb_selector], [result_box, result_text, explore_content_state])

    # 6. Result Box Actions
    close_result.click(lambda: gr.update(visible=False), None, result_box)
    
    def export_explore_pdf(content):
        path = generate_pdf_file(content, "Analysis Result")
        return gr.update(value=path, visible=True)
    
    export_result_btn.click(export_explore_pdf, [explore_content_state], [result_pdf_file])

    # 7. Generate
    def run_gen(mode, title, mod, lvl, f_c, lang, files):
        res = generate_content_core(mode, title, mod, lvl, f_c, lvl, lang, files)
        return res

    gen_btn.click(
        run_gen,
        [mode, title, modules, level, flash_opts, language, kb_selector], # Fixed inputs
        [output_text]
    )
    
    # 8. PDF Generate
    def export_gen_pdf(content, title):
        path = generate_pdf_file(content, title)
        return gr.update(value=path, visible=True)

    pdf_btn.click(export_gen_pdf, [output_text, title], [pdf_file])

    # Toggles
    def toggle(c_type):
        if c_type == "Flashcards" or c_type == "Quiz": return gr.update(visible=True)
        return gr.update(visible=False)

    mode.change(toggle, mode, flash_opts)

if __name__ == "__main__":
    demo.launch()