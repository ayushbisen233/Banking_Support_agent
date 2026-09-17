import os
import json
from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            self.client = None
        else:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                self.client = None
                
    def is_configured(self) -> bool:
        return self.client is not None

    def detect_intent(self, query: str, prompt_template: str) -> dict:
        """Detects intent and whether search is required based on the user query."""
        if not self.is_configured():
            return {"intent": "GENERAL", "requires_search": False, "error": "Gemini API key is missing or invalid."}
            
        try:
            prompt = prompt_template.replace("{query}", query)
            response = self.client.models.generate_content(
                model='gemini-3.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.0
                )
            )
            return json.loads(response.text)
        except Exception as e:
            # Mask error details if they contain sensitive info, but typically they don't here
            return {"intent": "GENERAL", "requires_search": False, "error": f"Failed to detect intent. {type(e).__name__}"}

    def generate_response(self, system_prompt: str, user_query: str, context: str = "") -> str:
        """Generates the final response for the user."""
        if not self.is_configured():
            return "Error: Gemini API is not properly configured. Please check your API key."
            
        try:
            full_prompt = f"{system_prompt}\n\n"
            if context:
                full_prompt += f"--- CONTEXT ---\n{context}\n---------------\n\n"
            full_prompt += f"User: {user_query}\nAgent:"
            
            response = self.client.models.generate_content(
                model='gemini-3.5-flash',
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3
                )
            )
            return response.text
        except Exception as e:
            return f"An error occurred while generating the response: {type(e).__name__}. Please try again later."
