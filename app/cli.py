import os
import sys
from typing import List
import typer
from dotenv import load_dotenv, set_key
from rich.console import Console
from app.assistant import Assistant

# Load configuration on startup
load_dotenv()

app = typer.Typer(help="Project Summer - Local AI Developer Assistant")
console = Console()

def run_chat(prompt: str, assistant: Assistant):
    """Stream response from Ollama via Assistant and print with rich styling."""
    console.print("[bold blue]Summer:[/bold blue] ", end="")
    try:
        in_thinking = False
        for chunk_type, text in assistant.send_message(prompt):
            if chunk_type == "thinking":
                if not in_thinking:
                    console.print("[Thinking: ", style="dim italic", end="", markup=False)
                    in_thinking = True
                console.print(text, style="dim italic", end="", markup=False)
            else:
                if in_thinking:
                    console.print("]\n", style="dim italic", end="", markup=False)
                    in_thinking = False
                console.print(text, end="", markup=False)
        if in_thinking:
            console.print("]", style="dim italic", end="", markup=False)
        console.print()
    except KeyboardInterrupt:
        console.print("\n[bold red][Stream interrupted][/bold red]")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Start Project Summer terminal assistant."""
    if ctx.invoked_subcommand is not None:
        return

    # Ensure stdout/stderr are UTF-8 on Windows
    if sys.platform == "win32":
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')

    assistant = Assistant()
    current_model = assistant.config.model_name or "auto-detected"
    
    console.print("[bold blue]╭──────────────────────────────────────────────╮[/bold blue]")
    console.print("[bold blue]│ Project Summer v0.1                          │[/bold blue]")
    console.print(f"[bold blue]│ Local Terminal Assistant (Model: {current_model:12.12}) │[/bold blue]")
    console.print("[bold blue]╰──────────────────────────────────────────────╯[/bold blue]")
    console.print("Type your message and press Enter. Type 'exit' or 'quit' to exit.")
    
    while True:
        try:
            user_input = console.input("\n[bold green]You:[/bold green] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold blue]Summer:[/bold blue] Goodbye!")
            break
        
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            console.print("[bold blue]Summer:[/bold blue] Goodbye!")
            break
            
        run_chat(user_input, assistant)

@app.command()
def chat(
    prompt: List[str] = typer.Argument(..., help="The prompt to send to Summer.")
):
    """Send a single prompt query to Summer."""
    if sys.platform == "win32":
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')

    assistant = Assistant()
    prompt_str = " ".join(prompt)
    run_chat(prompt_str, assistant)

@app.command()
def model():
    """Select the active Ollama model via an interactive table UI."""
    from rich.table import Table
    
    if sys.platform == "win32":
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
            
    assistant = Assistant()
    
    console.print("\n[bold blue]Scanning for local Ollama models...[/bold blue]\n")
    models = assistant.llm_client.get_installed_models()
    
    if not models:
        console.print("[bold red]Error: No local Ollama models found.[/bold red]")
        console.print("Please make sure Ollama is running and you have pulled at least one model.")
        raise typer.Exit(code=1)
        
    current_model = assistant.config.model_name
    
    table = Table(title="Available Ollama Models", show_header=True, header_style="bold blue")
    table.add_column("Index", style="dim", width=6)
    table.add_column("Model Name", style="bold green")
    table.add_column("Status", width=12)
    
    for idx, model_name in enumerate(models, 1):
        status = "[bold cyan]Active[/bold cyan]" if model_name == current_model else ""
        table.add_row(str(idx), model_name, status)
        
    console.print(table)
    
    try:
        choice = console.input("\nSelect a model by entering its number (or press Enter to cancel): ").strip()
        if not choice:
            console.print("[yellow]Selection cancelled.[/yellow]")
            return
            
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(models):
            selected_model = models[choice_idx]
            
            # Find/create .env path in workspace root
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            env_path = os.path.join(project_root, ".env")
            
            # Save key in .env file
            set_key(env_path, "OLLAMA_MODEL", selected_model)
            os.environ["OLLAMA_MODEL"] = selected_model
            
            console.print(f"\n[bold green]Success![/bold green] Active model set to: [bold cyan]{selected_model}[/bold cyan]")
        else:
            console.print("[bold red]Error: Invalid selection index.[/bold red]")
    except ValueError:
        console.print("[bold red]Error: Please enter a valid number.[/bold red]")

if __name__ == "__main__":
    app()
