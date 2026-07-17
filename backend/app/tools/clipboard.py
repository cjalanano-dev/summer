from typing import Dict, Any
import pyperclip
from app.tools.base import BaseTool

class ClipboardTool(BaseTool):
    """Allows Summer to access and update the system clipboard."""

    @property
    def name(self) -> str:
        return "clipboard"

    @property
    def description(self) -> str:
        return "Performs clipboard operations: read current text ('get'), copy new text ('set'), or empty the clipboard ('clear')."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["get", "set", "clear"],
                    "description": "The clipboard action: 'get' retrieves, 'set' updates, 'clear' wipes the clipboard."
                },
                "text": {
                    "type": "string",
                    "description": "The text to copy to the clipboard (required only if operation is 'set')."
                }
            },
            "required": ["operation"]
        }

    def execute(self, operation: str, text: str = None, **kwargs) -> Any:
        try:
            op = operation.strip().lower()
            if op == "get":
                clipboard_text = pyperclip.paste()
                if not clipboard_text:
                    return "Clipboard is empty."
                return f"Clipboard Content:\n{clipboard_text}"
            elif op == "set":
                if text is None:
                    return "Error: operation 'set' requires the 'text' parameter."
                pyperclip.copy(text)
                return "Successfully copied text to clipboard."
            elif op == "clear":
                pyperclip.copy("")
                return "Successfully cleared clipboard content."
            else:
                return f"Error: Unknown clipboard operation '{operation}'."
        except Exception as e:
            return f"Error: Clipboard operation failed. {str(e)}"
