import os
from app.workspace.detector import WorkspaceDetector
from app.workspace.scanner import WorkspaceScanner
from app.workspace.analyzer import WorkspaceAnalyzer
from app.workspace.models import Workspace

class WorkspaceManager:
    """Coordinating interface to detect, scan, analyze, and build workspace models."""
    
    def __init__(self, current_dir: str):
        self.current_dir = os.path.abspath(current_dir)
        self.detector = WorkspaceDetector(self.current_dir)
        self.root_path, self.is_project = self.detector.detect_project_root()
        
        self.scanner = WorkspaceScanner(self.root_path)
        self.analyzer = WorkspaceAnalyzer(self.root_path)
        self.workspace = None
        self.refresh()

    def refresh(self):
        """Re-scans and updates the cached active Workspace model state."""
        files, directories, total_size = self.scanner.scan()
        project_type, important_files, metadata = self.analyzer.analyze(files)
        project_name = os.path.basename(self.root_path)
        git_repository = os.path.exists(os.path.join(self.root_path, ".git"))
        
        self.workspace = Workspace(
            root_path=self.root_path,
            project_name=project_name,
            project_type=project_type,
            git_repository=git_repository,
            files=files,
            directories=directories,
            important_files=important_files,
            total_size=total_size,
            metadata=metadata
        )

    def get_workspace(self) -> Workspace:
        """Returns the current cached Workspace model, refreshing if directory changes."""
        current_cwd = os.path.abspath(os.getcwd())
        if current_cwd != self.detector.start_path:
            self.current_dir = current_cwd
            self.detector = WorkspaceDetector(self.current_dir)
            self.root_path, self.is_project = self.detector.detect_project_root()
            self.scanner = WorkspaceScanner(self.root_path)
            self.analyzer = WorkspaceAnalyzer(self.root_path)
            self.refresh()
        elif not self.workspace:
            self.refresh()
        return self.workspace

    def summary(self) -> str:
        """Returns a formatted human-readable summary of the active project workspace context."""
        ws = self.get_workspace()
        
        size_str = f"{ws.total_size} Bytes"
        if ws.total_size > 1024 * 1024:
            size_str = f"{ws.total_size / (1024 * 1024):.2f} MB"
        elif ws.total_size > 1024:
            size_str = f"{ws.total_size / 1024:.2f} KB"
            
        git_str = "Yes" if ws.git_repository else "No"
        
        ext_frequencies = ws.metadata.get("extensions", {})
        sorted_exts = sorted(ext_frequencies.items(), key=lambda x: x[1], reverse=True)
        ext_summary_lines = []
        for ext, count in sorted_exts:
            label = ext.upper().strip(".")
            ext_summary_lines.append(f"  {label} Files: {count}")
        ext_summary = "\n".join(ext_summary_lines) if ext_summary_lines else "  No extension files found."
        
        important_lines = []
        for f in ws.important_files:
            important_lines.append(f"  - {f}")
        important_summary = "\n".join(important_lines) if important_lines else "  None discovered."
        
        return (
            f"Project: {ws.project_name} ({ws.project_type})\n"
            f"Root: {ws.root_path}\n"
            f"Git Repository: {git_str}\n\n"
            f"Structure:\n"
            f"  Files: {len(ws.files)}\n"
            f"  Directories: {len(ws.directories)}\n"
            f"  Total Size: {size_str}\n\n"
            f"Languages / File Types:\n"
            f"{ext_summary}\n\n"
            f"Entry Points / Important Files:\n"
            f"{important_summary}"
        )
