import json
import re
from typing import List, Dict, Any
from app.llm import LLMClient

class Planner:
    """Decides if sub-tasks are needed and chooses appropriate tools or strategies using the LLM."""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def create_plan(self, prompt: str, history: List[Dict[str, str]], tools: List[Dict[str, Any]], model: str = None) -> Dict[str, Any]:
        """Examines the prompt and context to construct an execution plan using LLM routing."""
        # 1. Format the descriptions and properties of all tools
        tools_desc = []
        for t in tools:
            func = t.get("function", {})
            name = func.get("name")
            desc = func.get("description")
            params = func.get("parameters", {}).get("properties", {})
            required = func.get("parameters", {}).get("required", [])
            tools_desc.append(
                f"- Tool: '{name}'\n"
                f"  Description: {desc}\n"
                f"  Parameters: {params}\n"
                f"  Required arguments: {required}"
            )
        
        tools_description = "\n\n".join(tools_desc) if tools_desc else "No tools registered."
        
        # 2. Build the system query asking the model to select a tool or respond directly
        system_content = (
            "You are Summer's Planner Agent. Your job is to analyze the user's request and decide "
            "if it requires using one of the registered tools to answer correctly.\n\n"
            f"AVAILABLE TOOLS:\n{tools_description}\n\n"
            "INSTRUCTIONS:\n"
            "You must output a single, valid JSON block matching one of the following two schemas:\n\n"
            "If NO tool is needed, respond with:\n"
            "{\n"
            '  "type": "respond_direct",\n'
            '  "reason": "Explain why no tool is needed"\n'
            "}\n\n"
            "If a tool IS needed, respond with:\n"
            "{\n"
            '  "type": "execute_tool",\n'
            '  "tool_name": "<name_of_tool>",\n'
            '  "arguments": {\n'
            '    "<arg_name>": <arg_value>\n'
            "  }\n"
            "}\n\n"
            "CRITICAL: Do NOT output any markdown tags (like ```json or ```), explanation, or other text. "
            "Your output must be parseable by json.loads()."
        )
        
        # 3. Construct a temporary message thread to query the LLM Client
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"User query: \"{prompt}\"\n\nChoose the correct plan."}
        ]
        
        # 4. Call LLM (Planner calls with low temperature for stability)
        response_text = self.llm_client.chat(messages, model=model).strip()
        
        # 5. Clean up markdown JSON formatting if the model outputs it despite instructions
        clean_text = response_text
        if clean_text.startswith("```"):
            clean_text = re.sub(r"^```(?:json)?\n", "", clean_text)
            clean_text = re.sub(r"\n```$", "", clean_text)
        clean_text = clean_text.strip()
        
        # 6. Parse result
        try:
            plan = json.loads(clean_text)
            if isinstance(plan, dict) and "type" in plan:
                return plan
        except Exception:
            pass
            
        # Fallback to direct response
        return {
            "type": "respond_direct",
            "reason": "Failed to parse Planner LLM response or invalid format."
        }
