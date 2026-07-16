import re
from typing import Dict, Any
from app.tools.base import BaseTool

class CalculatorTool(BaseTool):
    """A tool that evaluates simple mathematical expressions safely."""

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Calculates mathematical expressions. Only supports simple arithmetic operators (+, -, *, /)."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate, e.g., '27 * 43'"
                }
            },
            "required": ["expression"]
        }

    def execute(self, expression: str, **kwargs) -> Any:
        # Strip all whitespace
        clean_expr = expression.replace(" ", "")
        
        # Validate that the string only contains numbers, decimal points, and math operators
        if not re.match(r"^[0-9.+\-*/()]+$", clean_expr):
            return "Error: Expression contains invalid characters. Only digits and operators (+, -, *, /, (, )) are allowed."
            
        try:
            # Safe evaluation using restricted eval environment after validation
            result = eval(clean_expr, {"__builtins__": None}, {})
            return str(result)
        except Exception as e:
            return f"Error: Failed to evaluate expression. {str(e)}"
