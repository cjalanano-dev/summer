import secrets
import string
from typing import Dict, Any
from app.tools.base import BaseTool

class PasswordGeneratorTool(BaseTool):
    """A tool that generates cryptographically secure passwords."""

    @property
    def name(self) -> str:
        return "password_generator"

    @property
    def description(self) -> str:
        return "Generates a cryptographically secure random password of specified length."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "length": {
                    "type": "integer",
                    "description": "The length of the password (defaults to 16)"
                }
            },
            "required": []
        }

    def execute(self, length: int = 16, **kwargs) -> Any:
        try:
            val_len = int(length)
            if val_len < 4:
                val_len = 4
                
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
            while True:
                password = "".join(secrets.choice(alphabet) for _ in range(val_len))
                if (any(c.isupper() for c in password)
                        and any(c.islower() for c in password)
                        and any(c.isdigit() for c in password)
                        and any(c in "!@#$%^&*()_+-=" for c in password)):
                    return password
        except Exception as e:
            return f"Error: Failed to generate password. {str(e)}"
