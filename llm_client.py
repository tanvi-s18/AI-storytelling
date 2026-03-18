from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
import json




class LLMClient:
    def __init__(self):
        self.enabled = bool(OPENAI_API_KEY)
        self.client = OpenAI(api_key=OPENAI_API_KEY) if self.enabled else None
        self.model = OPENAI_MODEL

    def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        if not self.enabled:
            raise RuntimeError("OPENAI_API_KEY not set.")

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.9,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return json.loads(response.choices[0].message.content)

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
        return response.choices[0].message.content.strip()
if __name__ == "__main__":
        client = LLMClient()
        print("enabled:", client.enabled)
        print(client.generate_text("You are helpful.", "Say hello in one sentence."))