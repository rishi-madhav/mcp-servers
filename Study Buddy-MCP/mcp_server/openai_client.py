"""OpenAI API client for generating educational content."""

import json
import os
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OpenAIClient:
    """Client for interacting with OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI client."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY not found. Set it in .env file or pass as parameter."
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"  # Fast, cheap, reliable
    
    async def generate_content(self, prompt: str) -> Dict[str, Any]:
        """
        Generate content using OpenAI API.
        
        Args:
            prompt: The prompt to send to OpenAI
            
        Returns:
            Parsed JSON response from OpenAI
        """
        try:
            # Generate content with JSON mode
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational tutor creating content for Indian students (grades 5-10) following CBSE/ICSE/IGCSE curriculum. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},  # Force JSON output
                temperature=0.7,
                max_tokens=2048
            )
            
            # Extract the response
            response_text = response.choices[0].message.content.strip()
            
            # Parse JSON
            try:
                result = json.loads(response_text)
                return result
            except json.JSONDecodeError as e:
                return {
                    "error": "Failed to parse JSON response from OpenAI",
                    "details": str(e),
                    "raw_response": response_text[:500],
                    "suggestion": "The AI returned invalid JSON. Try again."
                }
        
        except Exception as e:
            return {
                "error": f"OpenAI API error: {str(e)}",
                "suggestion": "Check your API key and internet connection."
            }

# Global client instance
_openai_client: Optional[OpenAIClient] = None

def get_openai_client() -> OpenAIClient:
    """Get or create the global OpenAI client instance."""
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAIClient()
    return _openai_client
