import json
import httpx
from typing import Generator, List

OLLAMA_URL = "http://localhost:11434"

def get_installed_models() -> List[str]:
    """Retrieve the list of installed models from local Ollama."""
    try:
        response = httpx.get(f"{OLLAMA_URL}/api/tags", timeout=5.0)
        if response.status_code == 200:
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
    except Exception:
        pass
    return []

def stream_chat(prompt: str, model: str = None) -> Generator[str, None, None]:
    """Send a prompt to Ollama and yield the response stream."""
    if not model:
        models = get_installed_models()
        if models:
            # Prioritize standard models
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
            model = "qwen2.5:latest"  # Fallback default

    try:
        with httpx.stream(
            "POST",
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": True
            },
            timeout=httpx.Timeout(180.0, connect=10.0, read=None)
        ) as response:
            if response.status_code != 200:
                yield "content", f"Error: Ollama returned status code {response.status_code}\n"
                return
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        message = chunk.get("message", {})
                        
                        # Handle thinking models (like qwen3.5 thinking, DeepSeek R1, etc.)
                        thinking = message.get("thinking", "")
                        if thinking:
                            yield "thinking", thinking
                        
                        content = message.get("content", "")
                        if content:
                            yield "content", content
                    except json.JSONDecodeError:
                        pass
    except httpx.ConnectError:
        yield "content", f"Error: Could not connect to Ollama at {OLLAMA_URL}. Is Ollama running?\n"
    except Exception as e:
        yield "content", f"Error: {str(e)}\n"
