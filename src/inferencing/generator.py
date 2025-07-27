import requests
import os
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union

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
    def __init__(self, model: Optional[str] = None) -> None:
        self.endpoint = os.getenv("INFERENCE_ENDPOINT")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {os.getenv("INFERENCE_API_KEY")}',
        }
        self.model = model
        
    def generate(self, messages: List[Union[Message, dict]], model: Optional[str] = None, **kwargs) -> dict:
        """Generate a response from the inference endpoint"""
        messages = [{**msg} for msg in messages]
        model = model or self.model
        if model is None:
            raise ValueError("No model specified in generator or generate call. Please specify a valid model to use for inference.")
        payload: dict = {"messages": messages, "model": model, **kwargs}
        response = requests.post(url=self.endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    generator = Generator()
    messages: List[Message | dict] = [
        {
            "role": "user",
            "content": "Hello, how are you?"
        }
    ]
    model: str = "gpt-4.1-nano"
    response = generator.generate(messages, model)
    