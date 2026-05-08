"""
🌏 MULTI-PROVIDER SUPPORT - Free & Chinese LLMs
DeepSeek, Qwen, Yi, Baichuan, Zhipu, and more
"""

import requests
import json
from typing import Optional, Dict, Any

class DeepSeekProvider:
    """DeepSeek API (Free tier available)"""
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY", "")
        self.base_url = "https://api.deepseek.com/v1"
        self.model = "deepseek-chat"
        self.total_cost = 0.0
    
    def query(self, prompt: str) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500
            }
            response = requests.post(f"{self.base_url}/chat/completions", 
                                    headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"ERROR: {response.status_code}"
        except Exception as e:
            return f"ERROR: {e}"
    
    def get_cost(self) -> float:
        return 0.0  # DeepSeek has free tier

class QwenProvider:
    """Alibaba Qwen (Free tier available via DashScope)"""
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY", "")
        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        self.model = "qwen-turbo"
        self.total_cost = 0.0
    
    def query(self, prompt: str) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "input": {"messages": [{"role": "user", "content": prompt}]},
                "parameters": {"max_tokens": 500}
            }
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()['output']['text']
            return f"ERROR: {response.status_code}"
        except Exception as e:
            return f"ERROR: {e}"
    
    def get_cost(self) -> float:
        return 0.0

class YiProvider:
    """01.AI Yi (Free API key available)"""
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("YI_API_KEY", "")
        self.base_url = "https://api.01.ai/v1/chat/completions"
        self.model = "yi-34b-chat-0205"
        self.total_cost = 0.0
    
    def query(self, prompt: str) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500
            }
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"ERROR: {response.status_code}"
        except Exception as e:
            return f"ERROR: {e}"
    
    def get_cost(self) -> float:
        return 0.0

class GroqProvider:
    """Groq (Fast free tier)"""
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-8b-8192"
        self.total_cost = 0.0
    
    def query(self, prompt: str) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500
            }
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"ERROR: {response.status_code}"
        except Exception as e:
            return f"ERROR: {e}"
    
    def get_cost(self) -> float:
        return 0.0

class TogetherProvider:
    """Together.ai (Free tier with rate limits)"""
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("TOGETHER_API_KEY", "")
        self.base_url = "https://api.together.xyz/v1/chat/completions"
        self.model = "meta-llama/Llama-3-8b-chat-hf"
        self.total_cost = 0.0
    
    def query(self, prompt: str) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500
            }
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"ERROR: {response.status_code}"
        except Exception as e:
            return f"ERROR: {e}"
    
    def get_cost(self) -> float:
        return 0.0

class OpenRouterProvider:
    """OpenRouter (Access to 100+ models, some free)"""
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "meta-llama/llama-3-8b-instruct:free"
        self.total_cost = 0.0
    
    def query(self, prompt: str) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500
            }
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"ERROR: {response.status_code}"
        except Exception as e:
            return f"ERROR: {e}"
    
    def get_cost(self) -> float:
        return 0.0

# Provider registry
PROVIDERS = {
    "1": {"name": "Ollama (Local, Free)", "class": None, "local": True},
    "2": {"name": "DeepSeek (Chinese, Free)", "class": DeepSeekProvider, "env_var": "DEEPSEEK_API_KEY"},
    "3": {"name": "Qwen (Alibaba, Free)", "class": QwenProvider, "env_var": "DASHSCOPE_API_KEY"},
    "4": {"name": "Yi (01.AI, Free)", "class": YiProvider, "env_var": "YI_API_KEY"},
    "5": {"name": "Groq (Fast, Free)", "class": GroqProvider, "env_var": "GROQ_API_KEY"},
    "6": {"name": "Together.ai (Free tier)", "class": TogetherProvider, "env_var": "TOGETHER_API_KEY"},
    "7": {"name": "OpenRouter (100+ free models)", "class": OpenRouterProvider, "env_var": "OPENROUTER_API_KEY"},
}
