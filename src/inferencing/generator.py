import requests
import os

class Generator:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.endpoint = os.getenv("INFERENCE_ENDPOINT")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {os.getenv("INFERENCE_API_KEY")}',
        }
        self.model = model
        
    def _create_payload(self, messages: list[dict]):
        return {"messages": messages, "model": self.model}
    
    def generate(self, messages: list[dict]):
        payload: dict = self._create_payload(messages=messages)
        response = requests.post(self.endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
