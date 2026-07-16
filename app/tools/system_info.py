import platform
import os
import shutil
from typing import Dict, Any
from app.tools.base import BaseTool

class SystemInfoTool(BaseTool):
    """A tool that gathers host platform and system metrics safely."""

    @property
    def name(self) -> str:
        return "system_info"

    @property
    def description(self) -> str:
        return "Gathers host platform metrics including OS version, CPU architecture, core count, and disk space usage."

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {},
            "required": []
        }

    def execute(self, **kwargs) -> Any:
        try:
            os_name = platform.system()
            os_release = platform.release()
            os_version = platform.version()
            cores = os.cpu_count() or "Unknown"
            arch = platform.machine()
            
            disk = shutil.disk_usage(".")
            total_gb = f"{disk.total / (1024**3):.2f} GB"
            used_gb = f"{disk.used / (1024**3):.2f} GB"
            free_gb = f"{disk.free / (1024**3):.2f} GB"
            
            info = (
                f"OS: {os_name} {os_release} ({os_version})\n"
                f"CPU Architecture: {arch}\n"
                f"CPU Cores: {cores}\n"
                f"Disk Usage (Total): {total_gb}\n"
                f"Disk Usage (Used): {used_gb}\n"
                f"Disk Usage (Free): {free_gb}"
            )
            return info
        except Exception as e:
            return f"Error: Failed to retrieve system info. {str(e)}"
