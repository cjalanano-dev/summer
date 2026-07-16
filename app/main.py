import sys

# Reconfigure stdout/stderr to use UTF-8 on Windows to prevent encoding errors with emojis/unicode
if sys.platform == "win32":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

from app.ollama import stream_chat


def run_chat(prompt: str):
    """Stream response from Ollama for a single prompt."""
    try:
        print("Summer: ", end="", flush=True)
        in_thinking = False
        for chunk_type, text in stream_chat(prompt):
            if chunk_type == "thinking":
                if not in_thinking:
                    # Enable dim gray color for thinking blocks
                    print("\033[90m[Thinking: ", end="", flush=True)
                    in_thinking = True
                print(text, end="", flush=True)
            else:
                if in_thinking:
                    # Reset formatting when moving to final content
                    print("]\033[0m\n", end="", flush=True)
                    in_thinking = False
                print(text, end="", flush=True)
        if in_thinking:
            print("]\033[0m")
        print()
    except KeyboardInterrupt:
        print("\n\033[0m[Stream interrupted]")

def main():
    """Main CLI entry point."""
    try:
        if len(sys.argv) > 1:
            # Single-shot command line arguments
            prompt = " ".join(sys.argv[1:])
            run_chat(prompt)
        else:
            # Interactive chat loop
            print("╭──────────────────────────────────────────────╮")
            print("│ Project Summer v0.1                          │")
            print("│ Local Terminal Assistant                      │")
            print("╰──────────────────────────────────────────────╯")
            print("Type your message and press Enter. Type 'exit' or 'quit' to exit.")
            
            while True:
                try:
                    prompt = input("\nYou: ").strip()
                except (KeyboardInterrupt, EOFError):
                    print("\nSummer: Goodbye!")
                    break

                if not prompt:
                    continue
                if prompt.lower() in ("exit", "quit"):
                    print("Summer: Goodbye!")
                    break
                
                run_chat(prompt)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
