# ☀️ Summer

**Summer** is a local-native AI assistant designed to run on your machine, leveraging local LLMs (via Ollama) and a rich suite of built-in developer tools, workspaces detection, and dynamic long-term memory. It features a modern, clean web interface alongside a flexible FastAPI backend.

---

## ✨ Features

- **Local LLM Integration:** Powered by [Ollama](https://ollama.com/), with support for models like `qwen2.5`, `llama3`, and others.
- **Agentic Loop (ReAct / Planning):** Features a Planner-Executor loop that dynamically selects and runs tools to fulfill complex requests.
- **Rich Tooling Suite:**
  - **File Operations:** Read file, search files, read multiple files.
  - **Workspace & System Info:** View active project summaries, directory listings, and system stats.
  - **Memory Tools:** Keep track of facts, projects, or preferences with `remember` and `forget` actions.
  - **Developer Utilities:** Base64, UUID generation, password generation, calculator, and clipboard integration.
- **Persistent Symbolic Memory:** Automatically extracts relevant facts, preferences, and details from your conversation history and stores them in a local SQLite database (`data/summer.db`).
- **Workspace Context Injection:** Dynamically scans your active workspace to provide contextually-aware responses to questions about your files and directory structure.
- **Modern SSE Chat Interface:** A React (Vite) single-page frontend that supports SSE streaming, reasoning/thinking model visualization, and model switching on the fly.

---

## 🏗️ Project Structure

```text
summer/
├── backend/
│   ├── app/
│   │   ├── agent/        # Planner and Executor logic
│   │   ├── api/          # FastAPI routers (chat, models, memory, workspace, health)
│   │   ├── memory/       # SQLite symbolic key-value memory subsystem
│   │   ├── tools/        # Built-in tool plugins (calculator, read_file, etc.)
│   │   ├── workspace/    # Project path scanner and analyzer
│   │   └── assistant.py  # Main Summer orchestrator class
│   ├── main.py           # FastAPI entrypoint
│   └── pyproject.toml    # Python configuration and dependencies
├── frontend/
│   ├── src/
│   │   ├── components/   # ChatWindow, Sidebar, ToolBadge, TopBar, etc.
│   │   ├── App.jsx       # Main UI component orchestrating SSE streams
│   │   └── index.css     # Premium styling sheet
│   └── package.json      # Node.js dependencies
└── README.md             # This documentation file
```

---

## 🚀 Getting Started

### Prerequisites

- **Python** (>= 3.10)
- **Node.js** (>= 18)
- **Ollama** installed and running locally

### 1. Set Up the Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -e .
   ```
4. Create a `.env` file in the `backend/` directory if you want to specify a default model:
   ```env
   OLLAMA_MODEL="qwen2.5:latest"
   ```
5. Run the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```
   *Note: If running from the root directory, use `uvicorn main:app --app-dir backend --reload`.*

### 2. Set Up the Frontend

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🛠️ Built-in Tools

Summer can automatically execute the following actions to help you work:
- **Calculator**: Evaluates math expressions.
- **Clipboard**: Reads or writes text to the system clipboard.
- **Directory List**: Inspects file structure in your directory.
- **Memory**: Adds/retrieves persistent context like preferences or facts.
- **System Info**: Checks operating system and environment specs.
- **Read & Search Files**: Inspects specific files or searches for queries inside code files.
- **Workspace Summary**: Automatically detects project structures (e.g. Git, React, Python) and provides a summary.

---

## 📝 Configuration

You can customize Summer's default behavior (e.g. system prompts, default model, temperature, theme) by modifying the `backend/config.toml` file:

```toml
default_model = "qwen2.5:latest"
temperature = 0.7
system_prompt = "app/prompts/system.txt"
stream = true
theme = "dark"
```
