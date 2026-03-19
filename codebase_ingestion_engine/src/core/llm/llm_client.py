import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

load_dotenv()

class LLMClient:
    def __init__(self):
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
        self.client = genai.Client()
        self.model_id = "gemini-3.1-flash-lite-preview"

    @retry(
        # We retry if '429' is in the error message
        retry=retry_if_exception_type(errors.ClientError),
        wait=wait_exponential(multiplier=2, min=10, max=60), # Increased min wait to 10s
        stop=stop_after_attempt(5),
        reraise=True
    )
    def generate(self, system_prompt, user_prompt):
        # Adding a small manual delay before every request 
        # prevents 'burst' 429 errors in Agent workflows.
        time.sleep(2) 

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.0,
                    max_output_tokens=8192,
                ),
            )
            return response.text
        except errors.ClientError as e:
            # Fix for AttributeError: Check string representation of the error
            error_msg = str(e).upper()
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print(f"⚠️ Quota reached. Tenacity will retry after a delay...")
                raise e 
            
            return f"❌ Permanent API Error: {e}"
        except Exception as e:
            return f"❌ Unexpected Error: {e}"