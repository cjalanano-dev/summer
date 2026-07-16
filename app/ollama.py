import ollama
from typing import Generator, List, Tuple

def get_installed_models() -> List[str]:
    """Retrieve the list of installed models from local Ollama."""
    try:
        response = ollama.list()
        return [model.get('model', model.get('name', '')) for model in response.get('models', [])]
    except Exception:
        pass
    return []

def stream_chat(prompt: str, model: str = None) -> Generator[Tuple[str, str], None, None]:
    """Send a prompt to Ollama and yield (chunk_type, text) response stream."""
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
        stream = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
        )
        for chunk in stream:
            message = chunk.get('message', {})
            
            # Handle thinking models
            thinking = message.get('thinking', '')
            if thinking:
                yield "thinking", thinking
            
            content = message.get('content', '')
            if content:
                yield "content", content
    except Exception as e:
        yield "content", f"Error: {str(e)}\n"
