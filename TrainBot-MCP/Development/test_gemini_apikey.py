import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')

print(f"API Key found: {api_key[:10]}..." if api_key else "NO API KEY FOUND!")
print(f"API Key length: {len(api_key) if api_key else 0}")

# Try to configure and list models
try:
    genai.configure(api_key=api_key)
    
    print("\n✅ Listing available models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
    
    print("\n🎯 Testing with gemini-1.5-flash:")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say 'Hello from Gemini!'")
    print(f"✅ SUCCESS: {response.text}")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")