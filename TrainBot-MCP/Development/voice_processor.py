"""
Voice Processor Module
Handles voice input (Gemini Audio) and voice output (ElevenLabs)
"""

import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Initialize clients
elevenlabs_client = ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY'))
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def transcribe_audio(audio_file_path):
    """
    Transcribe audio to text using Google Gemini
    
    Args:
        audio_file_path: Path to audio file (mp3, wav, etc.)
    
    Returns:
        str: Transcribed text
    """
    try:
        # Upload audio file to Gemini
        audio_file = genai.upload_file(path=audio_file_path)
        
        # Use Gemini to transcribe
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content([
            "Transcribe this audio exactly as spoken. Only output the transcription, nothing else.",
            audio_file
        ])
        
        # Clean up uploaded file
        genai.delete_file(audio_file.name)
        
        return response.text
        
    except Exception as e:
        raise Exception(f"Gemini audio transcription failed: {str(e)}")

def text_to_speech(text, voice_id="EXAVITQu4vr4xnSDxMaL"):
    """
    Convert text to speech using ElevenLabs
    
    Args:
        text: Text to convert to speech
        voice_id: ElevenLabs voice ID (default: Rachel)
    
    Returns:
        bytes: Audio data
    """
    try:
        # Generate audio using FREE TIER model
        audio_generator = elevenlabs_client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_turbo_v2"  # FREE tier model
        )
        
        # Collect audio bytes
        audio_bytes = b"".join(audio_generator)
        return audio_bytes
        
    except Exception as e:
        raise Exception(f"ElevenLabs synthesis failed: {str(e)}")

def save_audio(audio_data, output_path):
    """Save audio data to file"""
    with open(output_path, 'wb') as f:
        f.write(audio_data)
