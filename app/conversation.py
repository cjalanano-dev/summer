from typing import List, Dict

class Conversation:
    """Manages the active conversation history and message list."""
    
    def __init__(self, system_prompt: str = ""):
        self.messages: List[Dict[str, str]] = []
        if system_prompt:
            self.add_message("system", system_prompt)

    def add_message(self, role: str, content: str):
        """Append a new message to the history."""
        self.messages.append({"role": role, "content": content})

    def get_messages(self) -> List[Dict[str, str]]:
        """Return the conversation history."""
        return self.messages

    def clear(self, system_prompt: str = ""):
        """Clear conversation history, optionally setting a new system prompt."""
        self.messages = []
        if system_prompt:
            self.add_message("system", system_prompt)
