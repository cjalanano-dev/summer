import os
import ollama
from typing import Generator, List, Tuple

def load_system_prompt() -> str:
    """Read the system prompt from prompts/system.txt."""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(current_dir, "prompts", "system.txt")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read().strip()
    except Exception:
        pass
    return ""

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
        model = os.environ.get("OLLAMA_MODEL")
        
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
        system_prompt = load_system_prompt()
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})

        stream = ollama.chat(
            model=model,
            messages=messages,
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
