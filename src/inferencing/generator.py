import requests
import os
from dataclasses import dataclass
from enum import Enum
import json

class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"   

@dataclass
class Message:
    """Attributes:
        role: "user" | "assistant" | "system"
        content: str
    """
    role: Role
    content: str
    
    def __getitem__(self, key: str):
        if key == "role":
            return self.role.value
        elif key == "content":
            return self.content
        else:
            raise KeyError(key)
        
    def keys(self):
        return ["role", "content"]
    

class Generator:
    def __init__(self, model: str | None = None) -> None:
        self.endpoint: str = os.getenv("INFERENCE_ENDPOINT") or ""
        self.headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {os.getenv("INFERENCE_API_KEY")}',
        }
        self.model: str | None = model
        
    def generate(self, messages: list[Message] | list[dict[str, str]], model: str | None = None, **kwargs: dict[str, str]) -> dict[str, str]:
        """Generate a response from the inference endpoint"""
        messages = [{**msg} for msg in messages]
        model = model or self.model
        if model is None:
            raise ValueError("No model specified in generator or generate call. Please specify a valid model to use for inference.")
        payload = {"messages": messages, "model": model, **kwargs}
        response = requests.post(url=self.endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        response = {**response.json()}
        _ = self.validate_content(response)
        return response
    
    def validate_content(self, response: dict[str, str]) -> str:
        try:
            assert 'choices' in response and len(response['choices']) > 0
            choice = response['choices'][0]
            assert 'message' in choice and type(choice) is dict
            message = choice['message']
            assert 'content' in message and type(message) is dict
            assert type(message['content']) is str
            return message['content']
        except AssertionError:
            raise ValueError("Malformed response from the inference endpoint.")
        
    
    def generate_structured(self, messages: list[Message] | list[dict[str, str]], schema: dict[str, str], model: str | None = None, **kwargs: dict[str, str]) -> dict[str, str]:
        msgs: list[dict[str, str]] = [{**msg} for msg in messages]
        last_message: str = msgs[-1]['content']
        last_message = last_message + f"\n\nYOUR OUTPUT MUST FOLLOW THE FOLLOWING JSON SCHEMA:\n{schema}"
        msgs[-1]['content'] = last_message
        for _ in range(5):
            response = self.generate(msgs, model, **kwargs)
            try:
                content: str = self.validate_content(response)
                return {**json.loads(content)}
            except Exception as e:
                print(f"Failed to parse response: {e}")
        raise requests.exceptions.RetryError("Failed to generate structured response after 5 attempts.")
            