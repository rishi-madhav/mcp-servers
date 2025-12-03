"""
TrainBot - AI Training Course Generator
Enterprise-Grade Refactored Version
Architecture: Modular, Type-Safe, Error-Resistant
"""

import gradio as gr
import os
import time
import tempfile
import string  # Added for PDF character cleaning
from typing import List, Tuple, Optional, Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai
from fpdf import FPDF

# ============================================
# 🔧 CORE BUSINESS LOGIC (Separated from UI)
# ============================================

class TrainBotCore:
    """Core business logic for TrainBot - separated from UI"""
    
    def __init__(self):
        self.doc_store: Dict[str, str] = {}
        self.model_name = self._initialize_gemini()
        
    def _initialize_gemini(self) -> str:
        """Initialize Gemini API with fallback models"""
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            print("⚠️ WARNING: GEMINI_API_KEY not found.")
            return "models/gemini-1.5-flash"
            
        try:
            genai.configure(api_key=api_key)
            available = [m.name for m in genai.list_models() 
                        if 'generateContent' in m.supported_generation_methods]
            
            priority = [
                "models/gemini-2.5-flash", 
                "models/gemini-2.0-flash", 
                "models/gemini-1.5-pro",
                "models/gemini-1.5-flash"
            ]
            
            for model in priority:
                if model in available:
                    print(f"✅ Active Model: {model}")
                    return model
                    
            return "models/gemini-1.5-flash"
        except Exception as e:
            print(f"Gemini initialization error: {e}")
            return "models/gemini-1.5-flash"
    
    def process_file(self, file_obj) -> Tuple[Optional[str], str]:
        """Process uploaded file and store in document store"""
        if not file_obj:
            return None, "No file provided"
            
        try:
            filename = os.path.basename(file_obj.name)
            
            # Check if file already exists in document store
            if filename in self.doc_store:
                return None, f"File '{filename}' already processed (skipped)"
            
            content = ""
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
            
            # Only add to doc_store if processing was successful
            self.doc_store[filename] = content
            return filename, f"Successfully processed {filename} ({len(content)} characters)"
            
        except Exception as e:
            return None, f"Error processing file: {str(e)}"
    
    def process_youtube(self, url: str) -> Tuple[Optional[str], str]:
        """Process YouTube URL and extract transcript"""
        if not url.strip():
            return None, "No URL provided"
            
        try:
            # Extract video ID
            if "v=" in url:
                vid_id = url.split("v=")[1].split("&")[0]
            elif "youtu.be" in url:
                vid_id = url.split("/")[-1].split("?")[0]
            else:
                return None, "Invalid YouTube URL format"
            
            filename = f"YT_{vid_id}"
            
            # Check for duplicates
            if filename in self.doc_store:
                return None, f"Video '{vid_id}' already processed (skipped)"
            
            content = f"YouTube Video: {url}\nVideo ID: {vid_id}\n\n"
            
            try:
                from youtube_transcript_api import YouTubeTranscriptApi
                transcript = YouTubeTranscriptApi.get_transcript(vid_id)
                content += "Transcript:\n" + " ".join([t['text'] for t in transcript])
            except ImportError:
                content += "[YouTube transcript API not available]"
            except Exception as e:
                content += f"[Transcript unavailable: {str(e)}]"
            
            # Only add to doc_store after successful processing
            self.doc_store[filename] = content
            return filename, f"YouTube video {vid_id} processed successfully"
            
        except Exception as e:
            return None, f"YouTube processing error: {str(e)}"
    
    def chat_with_documents(self, message: str, selected_files: List[str]) -> str:
        """Chat with selected documents using Gemini"""
        if not message.strip():
            return "Please enter a question."
            
        try:
            # Build context from selected files
            context = ""
            if selected_files:
                for filename in selected_files:
                    if filename in self.doc_store:
                        content = self.doc_store[filename][:5000]  # Limit context
                        context += f"\n--- {filename} ---\n{content}\n"
            
            # Generate response
            model = genai.GenerativeModel(self.model_name)
            prompt = f"""You are a helpful assistant analyzing documents. 

Context from documents:
{context}

User question: {message}

Please provide a helpful response based on the document content. If the question isn't related to the documents, say so."""

            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def analyze_voice(self, audio_path: str, selected_files: List[str]) -> str:
        """Analyze voice recording with document context"""
        if not audio_path:
            return "Please record audio first."
            
        try:
            # Upload audio to Gemini
            myfile = genai.upload_file(audio_path)
            
            # Wait for processing
            while myfile.state.name == "PROCESSING":
                time.sleep(1)
                myfile = genai.get_file(myfile.name)
            
            # Build context
            context = ""
            if selected_files:
                for filename in selected_files:
                    if filename in self.doc_store:
                        content = self.doc_store[filename][:5000]
                        context += f"\n--- {filename} ---\n{content}\n"
            
            # Generate response
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content([
                f"Context from documents:\n{context}\n\nPlease answer the question in the audio file.",
                myfile
            ])
            
            return response.text
            
        except Exception as e:
            return f"Voice analysis error: {str(e)}"
    
    def summarize_documents(self, summary_type: str, selected_files: List[str]) -> str:
        """Generate summary of selected documents"""
        if not selected_files:
            return "Please select files to summarize."
            
        try:
            # Build content from selected files
            content = ""
            for filename in selected_files:
                if filename in self.doc_store:
                    file_content = self.doc_store[filename][:10000]  # Limit per file
                    content += f"\n--- {filename} ---\n{file_content}\n"
            
            if not content.strip():
                return "Selected files contain no readable content."
            
            # Generate summary
            model = genai.GenerativeModel(self.model_name)
            prompt = f"""Create a {summary_type.lower()} summary of the following documents:

{content}

Please provide a well-structured {summary_type.lower()} summary that captures the key points."""

            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Summary generation error: {str(e)}"
    
    def generate_course_content(self, mode: str, title: str, modules: int, 
                              level: str, flashcard_count: int, language: str, 
                              selected_files: List[str]) -> str:
        """Generate course content based on parameters"""
        try:
            # Build context from selected files
            context = ""
            if selected_files:
                for filename in selected_files:
                    if filename in self.doc_store:
                        content = self.doc_store[filename][:15000]  # Larger context for course generation
                        context += f"\n--- Source: {filename} ---\n{content}\n"
            
            # Generate appropriate prompt based on mode
            if mode == "Flashcards":
                prompt = f"""Create exactly {flashcard_count} educational flashcards on the topic "{title}".

Level: {level}
Language: {language}

Source material:
{context}

Format each flashcard as:
**Card X:**
**Question:** [Question here]
**Answer:** [Answer here]

Make them {level.lower()} level and ensure they test understanding of the key concepts."""

            elif mode == "Quiz":
                prompt = f"""Create a comprehensive quiz on "{title}" with 10 questions.

Level: {level}
Language: {language}

Source material:
{context}

Include:
- Multiple choice questions
- True/false questions
- Short answer questions

Format with clear numbering and answer key at the end."""

            elif mode == "Micro Course":
                prompt = f"""Create a concise micro-course on "{title}".

Level: {level}
Language: {language}

Source material:
{context}

Include:
- Brief introduction
- 3-4 key learning points
- Practical examples
- Quick assessment questions
- Summary

Keep it focused and actionable for busy learners."""

            else:  # Full Course
                prompt = f"""Create a comprehensive {modules}-module training course on "{title}".

Level: {level}
Language: {language}

Source material:
{context}

For each module, include:
- Learning objectives
- Key concepts explained
- Practical examples
- Activities or exercises
- Assessment questions

Structure it professionally with clear progression from basic to advanced concepts."""

            # Generate content
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Course generation error: {str(e)}"

# ============================================
# 📄 PDF GENERATION MODULE
# ============================================

class PDFGenerator:
    """Handles PDF generation with robust text cleaning and layout"""
    
    # Define character deletion table for control characters
    DELETE_CHARS = dict.fromkeys(
        i for i in range(128) if i < 32 or i == 127
    )
    
    @staticmethod
    def clean_text_for_pdf(text: str) -> str:
        """Clean text for PDF compatibility while preserving structure"""
        if not text:
            return ""
        
        # First, normalize line endings and preserve paragraph breaks
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove markdown formatting but preserve structure
        text = text.replace('**', '').replace('__', '')
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace("'", "'").replace("'", "'")
        text = text.replace('–', '-').replace('—', '-')
        
        # CRITICAL FIX: Replace ALL Unicode bullet characters with simple dash
        text = text.replace('•', '-')
        text = text.replace('●', '-')
        text = text.replace('▪', '-')
        text = text.replace('◦', '-')
        text = text.replace('▫', '-')
        
        # Remove control characters but preserve important whitespace
        # Only remove actual control characters (0-31, 127) not spaces/tabs/newlines
        DELETE_CHARS = dict.fromkeys(
            i for i in range(32) if i not in (9, 10, 13)  # Keep tab, LF, CR
        )
        DELETE_CHARS[127] = None  # DEL character
        text = text.translate(DELETE_CHARS)
        
        # AGGRESSIVE: Convert to ASCII early to catch any remaining Unicode
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            # First encode to ASCII, ignoring any characters that don't fit
            clean_line = line.encode('ascii', 'ignore').decode('ascii')
            cleaned_lines.append(clean_line)
        
        return '\n'.join(cleaned_lines)
    
    @staticmethod
    def create_pdf(content: str, title: str = "TrainBot Export") -> Optional[str]:
        """Create PDF file with proper formatting and structure"""
        if not content.strip():
            return None
            
        try:
            # Initialize PDF with explicit page format
            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.add_page()
            
            # Set all margins explicitly
            pdf.set_left_margin(15)
            pdf.set_right_margin(15)
            pdf.set_top_margin(15)
            pdf.set_auto_page_break(auto=True, margin=15)
            
            # Calculate usable width
            usable_width = 180  # 210mm - 30mm margins
            
            # Title section
            pdf.set_font("Helvetica", "B", 16)
            clean_title = PDFGenerator.clean_text_for_pdf(title)[:50]
            try:
                pdf.cell(usable_width, 10, clean_title, align="C")
                pdf.ln()  # Move to next line separately
            except:
                pdf.cell(usable_width, 10, "TrainBot Export", align="C")
                pdf.ln()
            
            pdf.ln(8)
            
            # Process content with proper formatting
            pdf.set_font("Helvetica", "", 11)
            clean_content = PDFGenerator.clean_text_for_pdf(content)
            
            # Split into paragraphs first
            paragraphs = clean_content.split('\n\n')
            
            for paragraph in paragraphs:
                if not paragraph.strip():
                    continue
                
                # Split paragraph into lines
                lines = paragraph.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        pdf.ln(3)  # Small space for empty lines
                        continue
                    
                    # Encode to Latin-1 early
                    safe_line = line.encode('latin-1', 'replace').decode('latin-1')
                    
                    # Handle different content types with better spacing
                    if line.startswith('###'):
                        # H3 Header
                        pdf.ln(3)  # Space before header
                        pdf.set_font("Helvetica", "B", 13)
                        header_text = safe_line.replace('#', '').strip()
                        try:
                            pdf.cell(usable_width, 8, header_text)
                            pdf.ln()  # Move to next line separately
                        except:
                            pdf.cell(usable_width, 8, "[Header]")
                            pdf.ln()
                        pdf.set_font("Helvetica", "", 11)
                        pdf.ln(2)  # Space after header
                        
                    elif line.startswith('##'):
                        # H2 Header
                        pdf.ln(4)  # More space before main header
                        pdf.set_font("Helvetica", "B", 14)
                        header_text = safe_line.replace('#', '').strip()
                        try:
                            pdf.cell(usable_width, 9, header_text)
                            pdf.ln()  # Move to next line separately
                        except:
                            pdf.cell(usable_width, 9, "[Header]")
                            pdf.ln()
                        pdf.set_font("Helvetica", "", 11)
                        pdf.ln(3)  # Space after header
                        
                    elif line.startswith('#'):
                        # H1 Header
                        pdf.ln(5)  # Even more space for main title
                        pdf.set_font("Helvetica", "B", 15)
                        header_text = safe_line.replace('#', '').strip()
                        try:
                            pdf.cell(usable_width, 10, header_text)
                            pdf.ln()  # Move to next line separately
                        except:
                            pdf.cell(usable_width, 10, "[Title]")
                            pdf.ln()
                        pdf.set_font("Helvetica", "", 11)
                        pdf.ln(4)
                        
                    elif line.startswith(('-', '*')):
                        # List items - Use simple ASCII dash (no Unicode bullets)
                        list_text = "- " + safe_line.lstrip('-*• ').strip()
                        try:
                            # Break long list items into multiple lines
                            pdf.multi_cell(usable_width, 6, list_text, border=0, align='L')
                        except:
                            pdf.multi_cell(usable_width, 6, "- [List item]")
                        pdf.ln(1)  # Small space after list item
                        
                    elif ':' in line and len(line.split(':')[0]) < 50:
                        # Definition or key-value pairs
                        try:
                            pdf.multi_cell(usable_width, 6, safe_line, border=0, align='L')
                        except:
                            pdf.multi_cell(usable_width, 6, "[Definition]")
                        pdf.ln(1)
                        
                    else:
                        # Regular paragraph text
                        try:
                            # Use multi_cell for automatic word wrapping
                            pdf.multi_cell(usable_width, 6, safe_line, border=0, align='L')
                        except:
                            pdf.multi_cell(usable_width, 6, "[Content could not be rendered]")
                        pdf.ln(1)
                
                # Add space between paragraphs
                pdf.ln(3)
            
            # Save file with ACTUAL dynamic naming - FIXED!
            timestamp = int(time.time())
            # Use the title parameter that was passed to create_pdf function
            clean_filename_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            clean_filename_title = clean_filename_title.replace(' ', '_')[:30]
            
            # If title is empty, use fallback
            if not clean_filename_title:
                clean_filename_title = "Export"
                
            filename = f"TrainBot_{clean_filename_title}_{timestamp}.pdf"
            filepath = os.path.join(tempfile.gettempdir(), filename)
            pdf.output(filepath)
            
            print(f"🎯 FILENAME DEBUG: Used title='{title}' → filename='{filename}'")
            
            return filepath
            
        except Exception as e:
            print(f"PDF generation error: {e}")
            return None

# ============================================
# 🎨 GRADIO UI (Clean and Modular)
# ============================================

def create_trainbot_interface():
    """Create the main TrainBot interface"""
    
    # Initialize core logic
    core = TrainBotCore()
    pdf_gen = PDFGenerator()
    
    # Theme for consistent look
    theme = gr.themes.Soft()
    
    with gr.Blocks(title="TrainBot - AI Course Architect") as interface:
        
        # State variables
        file_list_state = gr.State([])
        generated_content_state = gr.State("")
        
        # Header
        gr.Markdown("# 🎓 TrainBot: AI Course Architect")
        
        with gr.Row():
            
            # Left Column: Knowledge Base
            with gr.Column(scale=1, variant="panel"):
                gr.Markdown("### 📚 Knowledge Base")
                
                with gr.Tabs():
                    with gr.Tab("📄 Documents"):
                        file_upload = gr.File(
                            label="Upload Training Materials",
                            file_count="multiple",
                            file_types=[".pdf", ".docx", ".txt", ".mp3", ".mp4", ".csv", ".json"]
                        )
                    
                    with gr.Tab("🔗 YouTube"):
                        yt_url = gr.Textbox(
                            label="YouTube URL", 
                            placeholder="https://youtube.com/watch?v=...",
                            info="Extract transcript for training content"
                        )
                        yt_btn = gr.Button("Add Video", variant="secondary")
                
                gr.Markdown("### 🎯 Select Sources")
                kb_selector = gr.CheckboxGroup(
                    label="Active Files",
                    choices=[],
                    interactive=True,
                    info="Choose which files to use as context"
                )
                
                upload_status = gr.Markdown("**Ready to upload files...**")
            
            # Right Column: Workspace
            with gr.Column(scale=2):
                
                with gr.Tabs():
                    
                    # Explore Tab
                    with gr.Tab("🧭 Explore"):
                        gr.Markdown("### 💬 Chat with Your Documents")
                        
                        chatbot = gr.Chatbot(
                            height=350,
                            show_label=False,
                            placeholder="Your conversation will appear here..."
                        )
                        
                        with gr.Row():
                            chat_msg = gr.Textbox(
                                scale=4,
                                show_label=False,
                                placeholder="Ask questions about your uploaded content...",
                                container=False
                            )
                            chat_btn = gr.Button("Send", scale=1, variant="primary")
                        
                        gr.Markdown("---")
                        
                        with gr.Row():
                            with gr.Column():
                                gr.Markdown("### 🎤 Voice Analysis")
                                voice_input = gr.Audio(
                                    sources=["microphone"],
                                    type="filepath",
                                    label="Record your question"
                                )
                                voice_btn = gr.Button("Analyze Voice", variant="secondary")
                            
                            with gr.Column():
                                gr.Markdown("### 📝 Document Summary")
                                summary_type = gr.Dropdown(
                                    ["Executive", "Detailed", "Key Points"],
                                    value="Executive",
                                    label="Summary Type"
                                )
                                summary_btn = gr.Button("Generate Summary", variant="secondary")
                        
                        # Analysis Results
                        analysis_output = gr.Textbox(
                            label="Analysis Results",
                            lines=8,
                            visible=False,
                            show_copy_button=True
                        )
                        
                        with gr.Row(visible=False) as analysis_actions:
                            export_analysis_btn = gr.Button("📄 Export to PDF", variant="secondary")
                            analysis_pdf = gr.File(label="Download PDF", visible=False)
                    
                    # Generate Tab
                    with gr.Tab("✨ Generate Course"):
                        gr.Markdown("### ⚙️ Course Configuration")
                        
                        with gr.Row():
                            mode = gr.Dropdown(
                                ["Full Course", "Micro Course", "Quiz", "Flashcards"],
                                value="Full Course",
                                label="Content Type",
                                info="Choose the type of training content to generate"
                            )
                            language = gr.Dropdown(
                                ["English", "Spanish", "French", "German", "Hindi"],
                                value="English",
                                label="Language"
                            )
                        
                        title = gr.Textbox(
                            label="Course Title",
                            value="Professional Training Module",
                            placeholder="Enter a descriptive title..."
                        )
                        
                        # Course-specific options
                        with gr.Group(visible=True) as course_options:
                            with gr.Row():
                                modules = gr.Slider(
                                    1, 15, value=5, step=1,
                                    label="Number of Modules"
                                )
                                level = gr.Dropdown(
                                    ["Beginner", "Intermediate", "Advanced"],
                                    value="Intermediate",
                                    label="Difficulty Level"
                                )
                        
                        # Flashcard-specific options
                        with gr.Group(visible=False) as flashcard_options:
                            flashcard_count = gr.Slider(
                                5, 25, value=10, step=1,
                                label="Number of Flashcards"
                            )
                        
                        generate_btn = gr.Button(
                            "🚀 Generate Course Content",
                            variant="primary",
                            size="lg"
                        )
                        
                        gr.Markdown("### 📋 Generated Course")
                        course_output = gr.Textbox(
                            label="Your Training Content",
                            lines=20,
                            show_copy_button=True
                        )
                        
                        with gr.Row():
                            export_course_btn = gr.Button("📄 Export Course to PDF", variant="secondary")
                            course_pdf = gr.File(label="Download Course PDF", visible=False)
        
        # ============================================
        # 🔗 EVENT HANDLERS
        # ============================================
        
        # File Upload Handler
        def handle_file_upload(files, current_list):
            if not files:
                return gr.update(), current_list, "No files uploaded."
            
            new_files = []
            status_messages = []
            
            # Ensure current_list is a list and get existing filenames
            current_list = current_list or []
            existing_files = set(current_list)  # Use set for O(1) lookup
            
            for file in files:
                filename, message = core.process_file(file)
                if filename and filename not in existing_files:
                    new_files.append(filename)
                    existing_files.add(filename)  # Add to set to prevent duplicates in this batch
                status_messages.append(message)
            
            # Only add truly new files to the list
            updated_list = current_list + new_files
            status = "📁 **Upload Results:**\n" + "\n".join([f"• {msg}" for msg in status_messages])
            
            return (
                gr.update(choices=updated_list, value=updated_list),
                updated_list,
                status
            )
        
        file_upload.change(
            handle_file_upload,
            inputs=[file_upload, file_list_state],
            outputs=[kb_selector, file_list_state, upload_status]
        )
        
        # YouTube Handler
        def handle_youtube(url, current_list):
            filename, message = core.process_youtube(url)
            
            # Ensure current_list is a list
            current_list = current_list or []
            
            if filename and filename not in current_list:
                updated_list = current_list + [filename]
                return (
                    gr.update(choices=updated_list, value=updated_list),
                    updated_list,
                    f"🎥 **YouTube:** {message}",
                    ""  # Clear URL
                )
            else:
                # File already exists or error occurred
                return (
                    gr.update(),  # Don't update choices
                    current_list,  # Keep existing list
                    f"❌ **YouTube:** {message}",
                    url if not filename else ""  # Keep URL for retry if error, clear if duplicate
                )
        
        yt_btn.click(
            handle_youtube,
            inputs=[yt_url, file_list_state],
            outputs=[kb_selector, file_list_state, upload_status, yt_url]
        )
        
        # Chat Handler
        def handle_chat(message, history, selected_files):
            if not message.strip():
                return history, ""
            
            response = core.chat_with_documents(message, selected_files)
            
            # Ensure history is a list of lists
            if history is None:
                history = []
            
            history.append([message, response])
            return history, ""
        
        chat_btn.click(
            handle_chat,
            inputs=[chat_msg, chatbot, kb_selector],
            outputs=[chatbot, chat_msg]
        )
        
        chat_msg.submit(
            handle_chat,
            inputs=[chat_msg, chatbot, kb_selector],
            outputs=[chatbot, chat_msg]
        )
        
        # Voice Analysis Handler
        def handle_voice_analysis(audio, selected_files):
            result = core.analyze_voice(audio, selected_files)
            return (
                gr.update(value=result, visible=True),
                gr.update(visible=True)
            )
        
        voice_btn.click(
            handle_voice_analysis,
            inputs=[voice_input, kb_selector],
            outputs=[analysis_output, analysis_actions]
        )
        
        # Summary Handler
        def handle_summary(summary_type, selected_files):
            result = core.summarize_documents(summary_type, selected_files)
            return (
                gr.update(value=result, visible=True),
                gr.update(visible=True)
            )
        
        summary_btn.click(
            handle_summary,
            inputs=[summary_type, kb_selector],
            outputs=[analysis_output, analysis_actions]
        )
        
        # Course Generation Handler
        def handle_course_generation(mode, title, modules, level, f_count, language, selected_files):
            content = core.generate_course_content(
                mode, title, modules, level, f_count, language, selected_files
            )
            return content, content  # Update both display and state
        
        generate_btn.click(
            handle_course_generation,
            inputs=[mode, title, modules, level, flashcard_count, language, kb_selector],
            outputs=[course_output, generated_content_state]
        )
        
        # PDF Export Handlers
        def export_analysis_pdf(content):
            if not content:
                return gr.update()
            
            filepath = pdf_gen.create_pdf(content, "Analysis Results")
            if filepath:
                return gr.update(value=filepath, visible=True)
            return gr.update()
        
        export_analysis_btn.click(
            export_analysis_pdf,
            inputs=[analysis_output],
            outputs=[analysis_pdf]
        )
        
        # NOTE: Removed old export_course_pdf function - replaced by enhanced version below
        
        # UI Mode Switching
        def switch_mode(selected_mode):
            if selected_mode == "Flashcards":
                return (
                    gr.update(visible=False),  # course_options
                    gr.update(visible=True),   # flashcard_options
                    gr.update(placeholder="e.g., Data Science & Machine Learning")  # title placeholder
                )
            elif selected_mode == "Quiz":
                return (
                    gr.update(visible=True),   # course_options
                    gr.update(visible=False),  # flashcard_options
                    gr.update(placeholder="e.g., Data Science & Machine Learning")  # title placeholder
                )
            elif selected_mode == "Micro Course":
                return (
                    gr.update(visible=True),   # course_options
                    gr.update(visible=False),  # flashcard_options
                    gr.update(placeholder="e.g., Data Science & Machine Learning")  # title placeholder
                )
            else:  # Full Course
                return (
                    gr.update(visible=True),   # course_options
                    gr.update(visible=False),  # flashcard_options
                    gr.update(placeholder="e.g., Data Science & Machine Learning")  # title placeholder
                )
        
        # Enhanced Course Generation Handler with dynamic naming
        def handle_course_generation(mode, title, modules, level, f_count, language, selected_files):
            # Create dynamic title based on mode for the actual course generation
            if mode == "Micro Course":
                dynamic_title = f"Micro-Course: {title}"
            elif mode == "Quiz":
                dynamic_title = f"Quiz: {title}"
            elif mode == "Flashcards":
                dynamic_title = f"Flashcards: {title}"
            else:  # Full Course
                dynamic_title = title  # Keep original title
            
            content = core.generate_course_content(
                mode, dynamic_title, modules, level, f_count, language, selected_files
            )
            
            # Return content for both display and state
            return content, content
        
        generate_btn.click(
            handle_course_generation,
            inputs=[mode, title, modules, level, flashcard_count, language, kb_selector],
            outputs=[course_output, generated_content_state]
        )
        
        # Enhanced PDF Export for courses with dynamic naming
        def export_course_pdf_enhanced(content, base_title, mode):
            if not content:
                return gr.update()
            
            # Create dynamic PDF title - with debug output
            if mode == "Micro Course":
                pdf_title = f"Micro-Course: {base_title}"
            elif mode == "Quiz":
                pdf_title = f"Quiz: {base_title}"
            elif mode == "Flashcards":
                pdf_title = f"Flashcards: {base_title}"
            else:
                pdf_title = base_title
            
            print(f"🔍 DEBUG: PDF Export - Mode: {mode}, Base Title: {base_title}, PDF Title: {pdf_title}")
            
            filepath = pdf_gen.create_pdf(content, pdf_title)
            if filepath:
                print(f"✅ PDF Created: {filepath}")
                return gr.update(value=filepath, visible=True)
            return gr.update()
        
        export_course_btn.click(
            export_course_pdf_enhanced,
            inputs=[generated_content_state, title, mode],  # This should work correctly
            outputs=[course_pdf]
        )
        
        # Add the missing mode.change event handler
        mode.change(
            switch_mode,
            inputs=[mode],
            outputs=[course_options, flashcard_options, title]
        )
    
    return interface

# ============================================
# 🚀 MAIN APPLICATION
# ============================================

if __name__ == "__main__":
    # Create and launch interface
    demo = create_trainbot_interface()

    # FIX: Define the theme here before launch
    theme = gr.themes.Soft()

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
        theme=theme
    )