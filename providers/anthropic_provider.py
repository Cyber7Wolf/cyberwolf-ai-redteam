"""Anthropic Claude Provider Integration"""

import anthropic
from typing import Optional

class AnthropicProvider:
    def __init__(self, api_key: str, model: str = "claude-3-haiku-20240307"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.total_cost = 0.0
    
    def query(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Send query to Claude and return response"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Rough cost estimate (Claude 3 Haiku: $0.00025/1K input, $0.00125/1K output)
            input_cost = len(prompt) * 0.00000025
            output_cost = len(response.content[0].text) * 0.00000125
            self.total_cost += input_cost + output_cost
            
            return response.content[0].text
            
        except Exception as e:
            return f"ERROR: {e}"
    
    def get_cost(self) -> float:
        return self.total_cost
