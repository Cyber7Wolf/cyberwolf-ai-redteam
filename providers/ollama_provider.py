"""Ollama Local Provider (Free)"""

import requests
import json
from typing import Optional

class OllamaProvider:
    def __init__(self, model: str = "llama3.2:3b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.total_cost = 0.0
    
    def query(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Send query to local Ollama and return response"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": temperature
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get('response', 'No response')
            else:
                return f"ERROR: HTTP {response.status_code}"
                
        except Exception as e:
            return f"ERROR: {e}"
    
    def get_cost(self) -> float:
        return 0.0  # Ollama is free
