"""
LLM Runner abstraction
Supports local (Ollama) and cloud (OpenAI) backends
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.core.config import settings


class LLMDriver(ABC):
    """Abstract base class for LLM drivers"""
    
    @abstractmethod
    async def generate_summary(self, context: str, prompt_template: str) -> str:
        """Generate a summary from context"""
        pass
    
    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """Generate embeddings for text"""
        pass
    
    @abstractmethod
    async def available_models(self) -> List[str]:
        """Get list of available models"""
        pass


class LocalOllamaDriver(LLMDriver):
    """Ollama local LLM driver"""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
    
    async def generate_summary(self, context: str, prompt_template: str) -> str:
        """Generate summary using Ollama"""
        import httpx
        
        prompt = prompt_template.format(context=context)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=120.0,
            )
            response.raise_for_status()
            return response.json().get("response", "")
    
    async def embed(self, text: str) -> List[float]:
        """Generate embeddings using Ollama"""
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/embeddings",
                json={
                    "model": self.model,
                    "prompt": text,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json().get("embedding", [])
    
    async def available_models(self) -> List[str]:
        """Get available Ollama models"""
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            models = response.json().get("models", [])
            return [model.get("name", "") for model in models]


class OpenAIDriver(LLMDriver):
    """OpenAI cloud LLM driver"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
    
    async def generate_summary(self, context: str, prompt_template: str) -> str:
        """Generate summary using OpenAI"""
        from openai import AsyncOpenAI
        
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")
        
        client = AsyncOpenAI(api_key=self.api_key)
        prompt = prompt_template.format(context=context)
        
        response = await client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert OSINT analyst."},
                {"role": "user", "content": prompt},
            ],
        )
        
        return response.choices[0].message.content or ""
    
    async def embed(self, text: str) -> List[float]:
        """Generate embeddings using OpenAI"""
        from openai import AsyncOpenAI
        
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")
        
        client = AsyncOpenAI(api_key=self.api_key)
        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        
        return response.data[0].embedding
    
    async def available_models(self) -> List[str]:
        """Get available OpenAI models"""
        return [self.model, "gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]


class LLMRunner:
    """LLM runner service with driver abstraction"""
    
    def __init__(self):
        backend = settings.LLM_BACKEND.lower()
        
        if backend == "ollama":
            self.driver = LocalOllamaDriver()
        elif backend == "openai":
            self.driver = OpenAIDriver()
        else:
            raise ValueError(f"Unknown LLM backend: {backend}")
    
    async def generate_summary(self, context: str, prompt_template: str) -> str:
        """Generate summary using configured driver"""
        return await self.driver.generate_summary(context, prompt_template)
    
    async def embed(self, text: str) -> List[float]:
        """Generate embeddings using configured driver"""
        return await self.driver.embed(text)
    
    async def available_models(self) -> List[str]:
        """Get available models"""
        return await self.driver.available_models()












