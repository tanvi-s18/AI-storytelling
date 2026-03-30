#
# IMPORTS
# Architecture bucket:
#   Infrastructure / External Dependencies Layer
#
# - OpenAI: external LLM provider
# - config: environment/config management
# - json: response parsing layer
# 
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
import json



# LLM CLIENT (CORE MODEL INTERFACE)

# Architecture bucket:
#   LLM Abstraction Layer / Gateway
#
# Purpose:
# This class is the single interface between the application
# and OpenAI model.
#
# Everything in the system (crime setup, plot points, etc.)
# should call THIS instead of directly calling OpenAI.
#

class LLMClient:


    # Architecture bucket:
    #   Configuration + Dependency Injection
    #
    # What happens here:
    # - Checks if API key exists
    # - Initializes OpenAI client
    # - Stores model name
    #
   
    def __init__(self):
        self.enabled = bool(OPENAI_API_KEY)
        self.client = OpenAI(api_key=OPENAI_API_KEY) if self.enabled else None
        self.model = OPENAI_MODEL


   
    # Architecture bucket:
    #   Structured Generation Layer
    #   -> Used by:
    #      - Crime Setup Module
    #      - Suspense Frame Module
    #      - Suspects Module
    #      - Plot Point Generator
    #
    # Input:
    #   - system_prompt (global rules)
    #   - user_prompt (task-specific instruction)
    #
    # Output:
    #   - Parsed Python dict (JSON from model)
    #
  
    # Flow:
    #   Prompt → LLM → JSON string → parsed dict → returned
 
    def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        if not self.enabled:
            raise RuntimeError("OPENAI_API_KEY not set.")

        response = self.client.chat.completions.create(
            model=self.model,

            # Controls creativity vs determinism
            temperature=0.9,

            # Forces model to return valid JSON
            response_format={"type": "json_object"},

            # Prompt construction layer
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        # Output parsing layer
        return json.loads(response.choices[0].message.content)


    # Architecture bucket:
    #   Natural Language Generation Layer
    #   -> Used by:
    #      - Final Reveal (optional)
    #      - Story Retelling Module
    #
    # Input:
    #   - system_prompt
    #   - user_prompt
    #
    # Output:
    #   - Clean string (final narrative text)
    #
   
    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        if not self.enabled:
            raise RuntimeError("OPENAI_API_KEY not set.")

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.9,

            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        # Strip whitespace for cleaner downstream usage
        return response.choices[0].message.content.strip()



# Purpose:
# - Quick sanity check that:
#   - API key works
#   - model responds
#   - client wiring is correct
#

if __name__ == "__main__":
    client = LLMClient()

    # Check if API is configured
    print("enabled:", client.enabled)

    # Simple test call to verify end-to-end functionality
    print(client.generate_text(
        "You are helpful.",
        "Say hello in one sentence."
    ))