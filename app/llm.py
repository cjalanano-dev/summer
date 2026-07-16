import ollama
from typing import Generator, List, Tuple, Dict, Any
from app.config import Config

class LLMClient:
    """Handles direct communication with the local Ollama LLM service."""
    
    def __init__(self, config: Config):
        self.config = config

    def get_installed_models(self) -> List[str]:
        """Retrieve the list of installed models from local Ollama."""
        try:
            response = ollama.list()
            return [model.get('model', model.get('name', '')) for model in response.get('models', [])]
        except Exception:
            pass
        return []

    def stream_chat(self, messages: List[Dict[str, str]], model: str = None) -> Generator[Tuple[str, str], None, None]:
        """Send a message thread to Ollama and yield (chunk_type, text) response stream."""
        if not model:
            model = self.config.model_name
            
        if not model:
            models = self.get_installed_models()
            if models:
                preferred = ["qwen", "llama", "gemma", "deepseek"]
                selected = None
                for p in preferred:
                    for m in models:
                        if p in m.lower():
                            selected = m
                            break
                    if selected:
                        break
                model = selected if selected else models[0]
            else:
                model = "qwen2.5:latest"

        try:
            options = {
                "temperature": self.config.temperature
            }
            stream = ollama.chat(
                model=model,
                messages=messages,
                stream=self.config.stream,
                options=options
            )
            for chunk in stream:
                message = chunk.get('message', {})
                
                # Handle reasoning/thinking models
                thinking = message.get('thinking', '')
                if thinking:
                    yield "thinking", thinking
                
                content = message.get('content', '')
                if content:
                    yield "content", content
        except Exception as e:
            yield "content", f"Error: {str(e)}\n"
