import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Manages application-wide configurations and preferences."""
    
    def __init__(self):
        self.model_name = os.environ.get("OLLAMA_MODEL")
        self._system_prompt = None

    @property
    def system_prompt(self) -> str:
        """Dynamically loads and returns the system prompt from prompts/system.txt."""
        if self._system_prompt is None:
            self._system_prompt = self._load_system_prompt()
        return self._system_prompt

    def _load_system_prompt(self) -> str:
        """Reads the system prompt file."""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            prompt_path = os.path.join(current_dir, "prompts", "system.txt")
            if os.path.exists(prompt_path):
                with open(prompt_path, "r", encoding="utf-8") as f:
                    return f.read().strip()
        except Exception:
            pass
        return ""
