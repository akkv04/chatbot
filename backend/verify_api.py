import os
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI

def verify():
    load_dotenv()
    provider = os.getenv("LLM_PROVIDER", "google").lower()
    
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ Error: OPENAI_API_KEY not found in .env file.")
            return
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": "Hello, system check."}]
            )
            print("✅ Success: OpenAI API is working correctly!")
            print(f"Bot says: {response.choices[0].message.content}")
        except Exception as e:
            print(f"❌ Error: OpenAI check failed. Details: {str(e)}")
    else:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ Error: GOOGLE_API_KEY not found in .env file.")
            return
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("Hello, system check.")
            print("✅ Success: Gemini API is working correctly!")
            print(f"Bot says: {response.text}")
        except Exception as e:
            print(f"❌ Error: Gemini check failed. Details: {str(e)}")

if __name__ == "__main__":
    verify()
