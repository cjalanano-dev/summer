import os
import tomllib
from dotenv import load_dotenv

# Load environment variables from .env file on initialization
load_dotenv()

class Config:
    """Manages application-wide configurations loaded from config.toml and environment variables."""
    
    def __init__(self):
        # Resolve project root (one level up from app/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(current_dir)
        self.config_path = os.path.join(self.project_root, "config.toml")
        
        # Load defaults
        self.default_model = "qwen2.5:latest"
        self.temperature = 0.7
        self.system_prompt_path = "app/prompts/system.txt"
        self.stream = True
        self.theme = "dark"
        
        # Load from config.toml if it exists
        self._load_from_toml()

        # Environment variables can override toml config (e.g. OLLAMA_MODEL)
        self.model_name = os.environ.get("OLLAMA_MODEL") or self.default_model
        
        self._system_prompt = None

    def _load_from_toml(self):
        """Loads configuration keys from config.toml if it exists."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "rb") as f:
                    data = tomllib.load(f)
                    self.default_model = data.get("default_model", self.default_model)
                    self.temperature = data.get("temperature", self.temperature)
                    self.system_prompt_path = data.get("system_prompt", self.system_prompt_path)
                    self.stream = data.get("stream", self.stream)
                    self.theme = data.get("theme", self.theme)
            except Exception:
                pass

    @property
    def system_prompt(self) -> str:
        """Dynamically loads and returns the system prompt content."""
        if self._system_prompt is None:
            self._system_prompt = self._load_system_prompt()
        return self._system_prompt

    def _load_system_prompt(self) -> str:
        """Reads the system prompt file."""
        try:
            # Resolve system prompt path relative to project root if it is relative
            if not os.path.isabs(self.system_prompt_path):
                prompt_path = os.path.join(self.project_root, self.system_prompt_path)
            else:
                prompt_path = self.system_prompt_path
                
            if os.path.exists(prompt_path):
                with open(prompt_path, "r", encoding="utf-8") as f:
                    return f.read().strip()
        except Exception:
            pass
        return ""
