import re
from typing import List, Dict, Any

class Planner:
    """Decides if sub-tasks are needed and chooses appropriate tools or strategies."""
    
    def __init__(self):
        pass

    def create_plan(self, prompt: str, history: List[Dict[str, str]], tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Examines the prompt and context to construct an execution plan using simple rules."""
        prompt_lower = prompt.lower().strip()
        
        # 1. Current Time
        if any(w in prompt_lower for w in ["what time", "what date", "current time", "clock"]):
            return {
                "type": "execute_tool",
                "tool_name": "current_time",
                "arguments": {}
            }
            
        # 2. System Info
        if any(w in prompt_lower for w in ["system info", "cpu usage", "ram usage", "disk space", "system specification"]):
            return {
                "type": "execute_tool",
                "tool_name": "system_info",
                "arguments": {}
            }

        # 3. Directory List
        if "list" in prompt_lower and any(w in prompt_lower for w in ["file", "dir", "folder"]):
            path = "."
            match = re.search(r"(?:in|of|path)\s+([^\s]+)", prompt_lower)
            if match:
                candidate = match.group(1).strip("'\"?,.")
                if candidate not in ["the", "this", "current", "folder", "directory"]:
                    path = candidate
            return {
                "type": "execute_tool",
                "tool_name": "directory_list",
                "arguments": {"path": path}
            }

        # 4. Calculator
        if any(w in prompt_lower for w in ["calculate", "math", "evaluate", "what is"]):
            expression = ""
            for word in ["calculate", "evaluate", "what is"]:
                if word in prompt_lower:
                    idx = prompt_lower.find(word) + len(word)
                    expression = prompt[idx:].strip("? \t")
                    break
            
            if not expression:
                match = re.search(r"([0-9\s.+\-*/()]+)", prompt)
                if match:
                    expression = match.group(1).strip()
                    
            if expression:
                return {
                    "type": "execute_tool",
                    "tool_name": "calculator",
                    "arguments": {"expression": expression}
                }

        # 5. UUID Generator
        if any(w in prompt_lower for w in ["generate uuid", "generate guid", "create uuid"]):
            return {
                "type": "execute_tool",
                "tool_name": "uuid_generator",
                "arguments": {}
            }

        # 6. Password Generator
        if "password" in prompt_lower:
            length = 16
            match = re.search(r"(\d+)\s*(?:characters|char|length)?", prompt_lower)
            if match:
                length = int(match.group(1))
            return {
                "type": "execute_tool",
                "tool_name": "password_generator",
                "arguments": {"length": length}
            }

        # 7. Random Number
        if any(w in prompt_lower for w in ["random number", "pick a number", "roll"]):
            min_val = 1
            max_val = 100
            match = re.search(r"between\s+(\d+)\s+and\s+(\d+)", prompt_lower)
            if match:
                min_val = int(match.group(1))
                max_val = int(match.group(2))
            return {
                "type": "execute_tool",
                "tool_name": "random_number",
                "arguments": {"min_val": min_val, "max_val": max_val}
            }

        # Default: direct conversation
        return {
            "type": "respond_direct",
            "reason": "Direct communication."
        }
