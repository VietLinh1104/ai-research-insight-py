import google.generativeai as genai
import os
from dotenv import load_dotenv
import sys

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("NO API KEY FOUND")
    sys.exit(1)

genai.configure(api_key=api_key)

print(f"Using library version: {genai.__version__}")

print("\n--- Listing Models ---")
try:
    for m in genai.list_models():
        print(f"Model: {m.name}")
        print(f"Methods: {m.supported_generation_methods}")
except Exception as e:
    print(f"Error listing: {e}")

print("\n--- Testing Generation ---")
models_to_try = [
    'gemini-1.5-flash',
    'models/gemini-1.5-flash',
    'gemini-1.5-pro',
    'models/gemini-1.5-pro',
    'gemini-pro',
    'models/gemini-pro'
]

for model_name in models_to_try:
    print(f"\nTrying model: {model_name}")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        print(f"SUCCESS with {model_name}")
        break 
    except Exception as e:
        print(f"FAILED with {model_name}: {e}")
