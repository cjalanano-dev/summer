import json
import os
from typing import List, Dict

class Conversation:
    """Manages the active conversation history and message list."""
    
    def __init__(self, system_prompt: str = ""):
        self.messages: List[Dict[str, str]] = []
        self.system_prompt = system_prompt
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def add_user(self, content: str):
        """Append a user message to the history."""
        self.messages.append({"role": "user", "content": content})

    def add_assistant(self, content: str):
        """Append an assistant message to the history."""
        self.messages.append({"role": "assistant", "content": content})

    def clear(self):
        """Clear conversation history, resetting to system prompt."""
        self.messages = []
        if self.system_prompt:
            self.messages.append({"role": "system", "content": self.system_prompt})

    def save(self, filepath: str):
        """Save conversation history to a JSON file."""
        try:
            dir_name = os.path.dirname(os.path.abspath(filepath))
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump({
                    "system_prompt": self.system_prompt,
                    "messages": self.messages
                }, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def load(self, filepath: str):
        """Load conversation history from a JSON file."""
        try:
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.system_prompt = data.get("system_prompt", self.system_prompt)
                    self.messages = data.get("messages", [])
        except Exception:
            pass
