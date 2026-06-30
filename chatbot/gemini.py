import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

print("API KEY FOUND:", API_KEY)

# Configure Gemini
genai.configure(api_key=API_KEY)

# Create model
model = genai.GenerativeModel("gemini-2.5-flash")


def ask_gemini(prompt):

    system_prompt = f"""
You are ChatGPT, a professional AI assistant.

VERY IMPORTANT RULES:

1. Never answer in one long paragraph.
2. Always use proper Markdown formatting.
3. Use headings (##) whenever appropriate.
4. Use bullet points (-) or numbered lists (1. 2. 3.).
5. Keep answers concise and readable.
6. If the answer is a list, ALWAYS return a bullet list.
7. If code is needed, use triple backticks.
8. Only provide detailed explanations if the user explicitly asks for them.

User Question:
{prompt}
"""

    response = model.generate_content(system_prompt)

    return response.text