# Project Summer Architecture

This document describes the layered architecture of Project Summer.

## Overview

Summer is built around a decoupled layer pipeline to isolate CLI operations, agent loops, memory systems, tools, and the LLM client.

```
                  User
                   │
         ┌─────────┴─────────┐
         │                   │
     Terminal            Voice (Future)
         │                   │
         └─────────┬─────────┘
                   │
                Summer (Coordinator)
                   │
     ┌─────────────┼─────────────┐
     │             │             │
Conversation    Memory        Planner
     │             │             │
     └─────────────┼─────────────┘
                   │
              Tool Manager
                   │
             Ollama Client
```

## Layer Breakdown

1. **CLI / Interface Layer (`app/cli.py`)**:
   Handles console parsing, styling (Rich), interactive callbacks, and slash command interception. The CLI knows nothing about AI.
2. **Coordinator Layer (`app/assistant.py`)**:
   Exposes the central `Summer` class. Unifies configurations, active conversation threads, and persistent transaction logging.
3. **Conversation Layer (`app/conversation.py`)**:
   Manages message threads (`messages` list) with role helpers (`add_user`, `add_assistant`) and serialization/deserialization methods.
4. **Agent Loop Layer (`app/agent/`)**:
   - `Agent` (orchestrates loop steps)
   - `Planner` (evaluates context to build execution tasks or tool selections)
   - `Executor` (runs scheduled actions and aggregates outcomes)
5. **Tooling Layer (`app/tools/`)**:
   Exposes the abstract class `BaseTool` and `ToolManager` to register and execute tools through a standard interface.
6. **LLM Client Layer (`app/llm.py`)**:
   Wraps communications with local Ollama service, managing fallbacks, options (like temperature), and streams.
