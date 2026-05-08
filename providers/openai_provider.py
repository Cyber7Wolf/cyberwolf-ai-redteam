"""OpenAI GPT Provider Integration"""

import openai
from typing import Optional

class OpenAIProvider:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.total_tokens = 0
        self.total_cost = 0.0
    
    def query(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Send query to OpenAI and return response"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Track usage
            self.total_tokens += response.usage.total_tokens
            # Cost calculation (gpt-3.5-turbo: $0.0015/1K input, $0.002/1K output)
            input_cost = response.usage.prompt_tokens * 0.0000015
            output_cost = response.usage.completion_tokens * 0.000002
            self.total_cost += input_cost + output_cost
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"ERROR: {e}"
    
    def get_cost(self) -> float:
        return self.total_cost
