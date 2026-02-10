import google.generativeai as genai
import os
from dotenv import load_dotenv
import sys

# Redirect stdout to a file to avoid truncation issues in terminal output capture
sys.stdout = open('model_debug.log', 'w', encoding='utf-8')

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: No API Key found in environment variables.")
    sys.exit(1)

print(f"API Key found (starts with): {api_key[:5]}...")

genai.configure(api_key=api_key)

print(f"Library version: {genai.__version__}")

print("\n--- Listing Available Models ---")
available_models = []
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Found supported model: {m.name}")
            available_models.append(m.name)
except Exception as e:
    print(f"ERROR listing models: {str(e)}")

print(f"\nTotal supported models found: {len(available_models)}")

if not available_models:
    print("CRITICAL: No models found capable of generateContent.")
    print("Possibilities: API Key invalid, Expired, or has no model access.")
else:
    print("\n--- Testing Generation with Found Models ---")
    working_model = None
    for model_name in available_models:
        print(f"Testing {model_name}...")
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Test")
            print(f"SUCCESS: {model_name} works!")
            working_model = model_name
            break
        except Exception as e:
            print(f"FAILED {model_name}: {str(e)}")
    
    if working_model:
        print(f"\nRECOMMENDATION: Use model '{working_model}'")
    else:
        print("\nCRITICAL: Found models but none could generate content.")
