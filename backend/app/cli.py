import os
import sys
from typing import List
import typer
from dotenv import load_dotenv, set_key
from rich.console import Console
from app.assistant import Summer

# Load configuration on startup
load_dotenv()

app = typer.Typer(help="Project Summer - Local AI Developer Assistant")
console = Console()

def run_chat(prompt: str, summer: Summer):
    """Stream response from Ollama via Summer and print with rich styling."""
    console.print("[bold blue]Summer:[/bold blue] ", end="")
    try:
        in_thinking = False
        for chunk_type, text in summer.chat(prompt):
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

def change_model_interactive(summer: Summer):
    """Interactive helper to switch local Ollama models."""
    from rich.table import Table
    
    console.print("\n[bold blue]Scanning for local Ollama models...[/bold blue]\n")
    models = summer.llm_client.get_installed_models()
    
    if not models:
        console.print("[bold red]Error: No local Ollama models found.[/bold red]")
        console.print("Please make sure Ollama is running and you have pulled at least one model.")
        return
        
    current_model = summer.config.model_name
    
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
            summer.config.model_name = selected_model
            
            console.print(f"\n[bold green]Success![/bold green] Active model set to: [bold cyan]{selected_model}[/bold cyan]")
        else:
            console.print("[bold red]Error: Invalid selection index.[/bold red]")
    except ValueError:
        console.print("[bold red]Error: Please enter a valid number.[/bold red]")

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

    summer = Summer()
    current_model = summer.config.model_name or "auto-detected"
    
    console.print("[bold blue]╭──────────────────────────────────────────────╮[/bold blue]")
    console.print("[bold blue]│ Project Summer v0.1                          │[/bold blue]")
    console.print(f"[bold blue]│ Local Terminal Assistant (Model: {current_model:12.12}) │[/bold blue]")
    console.print("[bold blue]╰──────────────────────────────────────────────╯[/bold blue]")
    console.print("Type your message and press Enter. Type /help to see commands, or /exit to exit.")
    
    while True:
        try:
            user_input = console.input("\n[bold green]You:[/bold green] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold blue]Summer:[/bold blue] Goodbye!")
            break
        
        if not user_input:
            continue

        # Intercept Slash Commands
        if user_input.startswith("/"):
            parts = user_input.split()
            cmd = parts[0].lower()
            
            if cmd == "/exit":
                console.print("[bold blue]Summer:[/bold blue] Goodbye!")
                break
            elif cmd == "/help":
                console.print("\n[bold blue]Available Slash Commands:[/bold blue]")
                console.print("  [bold green]/help[/bold green]              - Show this help message")
                console.print("  [bold green]/clear[/bold green]             - Clear the console and reset conversation history")
                console.print("  [bold green]/history[/bold green]           - Display the conversation history so far")
                console.print("  [bold green]/model[/bold green]             - Switch active Ollama models interactively")
                console.print("  [bold green]/config[/bold green]            - Print current application configurations")
                console.print("  [bold green]/about[/bold green]             - Print information about Project Summer")
                console.print("  [bold green]/refresh-workspace[/bold green]   - Recrawl workspace directories and rebuild summary")
                console.print("  [bold green]/remember <category> <key> = <value>[/bold green]   - Manually save a fact to memory")
                console.print("  [bold green]/forget <id>[/bold green]       - Delete a memory by its ID")
                console.print("  [bold green]/memory[/bold green]            - List all stored memories")
                console.print("  [bold green]/search-memory <q>[/bold green] - Search stored memories")
                console.print("  [bold green]/clear-memory[/bold green]      - Delete all stored memories")
                console.print("  [bold green]/exit[/bold green]              - Exit the interactive session")
            elif cmd == "/refresh-workspace":
                summer.workspace.refresh()
                console.print("[bold green]Workspace crawled files and configurations reloaded successfully.[/bold green]")
                console.print(summer.workspace.summary())
            elif cmd == "/clear":
                summer.conversation.clear()
                os.system('cls' if os.name == 'nt' else 'clear')
                console.print("[bold green]Conversation history cleared and screen reset.[/bold green]")
            elif cmd == "/history":
                console.print("\n[bold blue]Conversation History:[/bold blue]\n")
                if not summer.conversation.messages or len(summer.conversation.messages) <= 1:
                    console.print("[dim]No messages in history yet.[/dim]")
                else:
                    for msg in summer.conversation.messages:
                        role = msg["role"]
                        content = msg["content"]
                        if role == "system":
                            continue
                        style = "bold green" if role == "user" else "bold blue"
                        name = "You" if role == "user" else "Summer"
                        console.print(f"[{style}]{name}:[/{style}] {content}")
            elif cmd == "/model":
                change_model_interactive(summer)
            elif cmd == "/config":
                console.print("\n[bold blue]Configurations:[/bold blue]")
                console.print(f"  [bold]Active Model:[/bold] {summer.config.model_name or 'auto-detected'}")
                current_dir = os.path.dirname(os.path.abspath(__file__))
                prompt_path = os.path.join(current_dir, "prompts", "system.txt")
                console.print(f"  [bold]System Prompt Path:[/bold] {prompt_path}")
            elif cmd == "/about":
                console.print("\n[bold blue]About Project Summer:[/bold blue]")
                console.print("  A terminal-native local AI developer assistant running on Ollama.")
                console.print("  Designed with a modular, agent-ready architecture.")
            elif cmd == "/remember":
                content = " ".join(parts[1:]).strip()
                if not content or "=" not in content:
                    console.print("[bold red]Usage: /remember <category> <key> = <value>[/bold red]")
                    console.print("Example: /remember preference editor = VS Code")
                else:
                    try:
                        left, right = content.split("=", 1)
                        value = right.strip()
                        left_parts = left.strip().split(None, 1)
                        if len(left_parts) < 2:
                            console.print("[bold red]Usage: /remember <category> <key> = <value>[/bold red]")
                        else:
                            category, key = left_parts
                            mem_id = summer.memory.remember(category, key, value)
                            console.print(f"[bold green]Saved to memory (ID: {mem_id}) under category '{category.lower()}'.[/bold green]")
                    except Exception as e:
                        console.print(f"[bold red]Error saving memory: {str(e)}[/bold red]")
            elif cmd == "/forget":
                if len(parts) < 2:
                    console.print("[bold red]Usage: /forget <memory_id>[/bold red]")
                else:
                    try:
                        mem_id = int(parts[1])
                        success = summer.memory.forget(mem_id)
                        if success:
                            console.print(f"[bold green]Deleted memory with ID {mem_id}.[/bold green]")
                        else:
                            console.print(f"[bold red]Memory with ID {mem_id} not found.[/bold red]")
                    except ValueError:
                        console.print("[bold red]Error: Memory ID must be an integer.[/bold red]")
            elif cmd in ("/memory", "/memories"):
                memories = summer.memory.list_memories()
                if not memories:
                    console.print("[dim]No memories stored yet.[/dim]")
                else:
                    grouped = {}
                    for m in memories:
                        cat = m.category.capitalize()
                        if cat not in grouped:
                            grouped[cat] = []
                        grouped[cat].append(m)
                    
                    console.print("\n[bold blue]Summer Memory[/bold blue]\n")
                    for cat, items in grouped.items():
                        console.print(f"[bold green]{cat}[/bold green]")
                        console.print(f"[dim]{'-' * len(cat)}[/dim]")
                        for m in items:
                            console.print(f"  [bold cyan]{m.key}[/bold cyan] (ID: {m.id})")
                            console.print(f"  {m.value}\n")
            elif cmd == "/search-memory":
                q = " ".join(parts[1:]).strip()
                if not q:
                    console.print("[bold red]Usage: /search-memory <query>[/bold red]")
                else:
                    from rich.table import Table
                    results = summer.memory.search(q)
                    if not results:
                        console.print(f"[dim]No memories matching '{q}' found.[/dim]")
                    else:
                        table = Table(title=f"Memory Search Results: '{q}'", show_header=True, header_style="bold blue")
                        table.add_column("ID", style="dim", width=6)
                        table.add_column("Category", style="bold green", width=15)
                        table.add_column("Key", style="bold cyan", width=15)
                        table.add_column("Value")
                        table.add_column("Importance", style="dim", width=12)
                        for m in results:
                            table.add_row(str(m.id), m.category.capitalize(), m.key, m.value, str(m.importance))
                        console.print(table)
            elif cmd == "/clear-memory":
                summer.memory.clear_all()
                console.print("[bold green]All stored memories deleted.[/bold green]")
            continue
            
        run_chat(user_input, summer)

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

    summer = Summer()
    prompt_str = " ".join(prompt)
    run_chat(prompt_str, summer)

@app.command()
def model():
    """Select the active Ollama model via an interactive table UI."""
    if sys.platform == "win32":
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
            
    summer = Summer()
    change_model_interactive(summer)

if __name__ == "__main__":
    app()
