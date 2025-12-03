"""Google Gemini API client for generating educational content."""

import json
import os
import re
from typing import Dict, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiClient:
    """Client for interacting with Google Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini client."""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Set it in .env file or pass as parameter."
            )
        
        genai.configure(api_key=self.api_key)
        
        # Safety settings to reduce false positives
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]
        
        # Use Gemini 2.0 Flash Experimental (available in your API key)
        # Note: We've set safety to BLOCK_NONE for educational content
        self.model = genai.GenerativeModel(
            'gemini-2.0-flash-exp',  # The model available in your API key
            generation_config={
                "temperature": 0.3,  # Even lower for more predictable output
                "top_p": 0.8,
                "top_k": 20,
                "max_output_tokens": 2048,
                "response_mime_type": "application/json",
            },
            safety_settings=safety_settings
        )
    
    async def generate_content(self, prompt: str, max_retries: int = 3) -> Dict[str, Any]:
        """
        Generate content using Gemini API with retry logic.
        
        Args:
            prompt: The prompt to send to Gemini
            max_retries: Maximum number of retry attempts
            
        Returns:
            Parsed JSON response from Gemini
        """
        for attempt in range(max_retries):
            try:
                # Generate content
                response = self.model.generate_content(prompt)
                
                # Check if response was blocked by safety filters
                if not response.candidates:
                    return {
                        "error": "Content blocked by safety filters",
                        "suggestion": "Try rephrasing your query with different wording."
                    }
                
                # Check finish reason
                candidate = response.candidates[0]
                if hasattr(candidate, 'finish_reason'):
                    if candidate.finish_reason == 2:  # SAFETY
                        return {
                            "error": "Response blocked for safety reasons",
                            "suggestion": "Try a different topic or rephrase your question."
                        }
                    elif candidate.finish_reason == 3:  # RECITATION
                        return {
                            "error": "Response blocked due to recitation concerns",
                            "suggestion": "Try asking in a different way."
                        }
                
                # Extract text from response
                response_text = response.text.strip()
                
                # Clean up the response
                response_text = self._clean_json_response(response_text)
                response_text = self._fix_json_issues(response_text)
                
                # Parse JSON
                try:
                    result = json.loads(response_text)
                    return result
                except json.JSONDecodeError as e:
                    if attempt < max_retries - 1:
                        # Retry with slightly modified prompt
                        continue
                    else:
                        # Last attempt - try to extract partial JSON
                        partial_result = self._try_partial_json(response_text)
                        if partial_result:
                            return partial_result
                        
                        return {
                            "error": "Failed to parse JSON response from Gemini",
                            "details": str(e),
                            "raw_response": response_text[:500],
                            "suggestion": "The AI returned invalid JSON. Try rephrasing your query or try again."
                        }
            
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                else:
                    return {
                        "error": f"Gemini API error: {str(e)}",
                        "suggestion": "Check your API key and internet connection, or try again."
                    }
        
        return {
            "error": "Max retries exceeded",
            "suggestion": "Please try again."
        }
    
    def _try_partial_json(self, text: str) -> Dict[str, Any] | None:
        """
        Try to extract and fix partial/broken JSON.
        
        Args:
            text: Broken JSON text
            
        Returns:
            Dict if successful, None otherwise
        """
        try:
            # Find the last complete key-value pair before the break
            # Add closing braces if needed
            if text.count('{') > text.count('}'):
                text = text + '"}' * (text.count('{') - text.count('}'))
            
            # Try parsing again
            return json.loads(text)
        except:
            return None
    
    def _fix_json_issues(self, text: str) -> str:
        """
        Fix common JSON issues in Gemini responses.
        
        Args:
            text: Raw JSON text
            
        Returns:
            Cleaned JSON string
        """
        # Replace curly quotes with straight quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace("'", "'").replace("'", "'")
        
        # Fix unescaped newlines within strings (common issue)
        # This is a simple approach - replace \n not preceded by \
        import re
        # Find strings and escape newlines within them
        # Note: This is a simplified fix and may not catch all cases
        
        # Remove any trailing commas before closing braces/brackets
        text = re.sub(r',(\s*[}\]])', r'\1', text)
        
        return text
    
    def _clean_json_response(self, text: str) -> str:
        """
        Clean JSON response by removing markdown code blocks.
        
        Args:
            text: Raw response text
            
        Returns:
            Cleaned JSON string
        """
        # Remove markdown code blocks (```json ... ``` or ``` ... ```)
        text = re.sub(r'^```(?:json)?\s*\n', '', text, flags=re.MULTILINE)
        text = re.sub(r'\n```\s*$', '', text, flags=re.MULTILINE)
        
        # Remove any leading/trailing whitespace
        text = text.strip()
        
        return text

# Global client instance
_gemini_client: Optional[GeminiClient] = None

def get_gemini_client() -> GeminiClient:
    """Get or create the global Gemini client instance."""
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client
