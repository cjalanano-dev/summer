import sys
from typing import List
import typer
from rich.console import Console
from app.ollama import stream_chat

app = typer.Typer(help="Project Summer - Local AI Developer Assistant")
console = Console()

def run_chat(prompt: str):
    """Stream response from Ollama and print with rich styling."""
    console.print("[bold blue]Summer:[/bold blue] ", end="")
    try:
        in_thinking = False
        for chunk_type, text in stream_chat(prompt):
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

@app.command()
def main(
    prompt: List[str] = typer.Argument(None, help="The prompt to send to Summer. If empty, starts interactive session.")
):
    """Start Project Summer terminal assistant."""
    # Ensure stdout/stderr are UTF-8 on Windows
    if sys.platform == "win32":
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')

    if prompt:
        prompt_str = " ".join(prompt)
        run_chat(prompt_str)
    else:
        console.print("[bold blue]╭──────────────────────────────────────────────╮[/bold blue]")
        console.print("[bold blue]│ Project Summer v0.1                          │[/bold blue]")
        console.print("[bold blue]│ Local Terminal Assistant                     │[/bold blue]")
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
                
            run_chat(user_input)

if __name__ == "__main__":
    app()
