# Project Summer Roadmap

This document outlines the milestones and future plans for Project Summer.

## Phase 1: MVP Chat Interface (Complete)
- [x] Stream chat outputs.
- [x] Interactive model selector with `.env` persistence.
- [x] Simple Typer CLI setup.

## Phase 2: Decoupled Foundation (Complete)
- [x] Decouple CLI, Summer coordinator, Conversation history, LLMClient, Config manager.
- [x] Refactor Agent into Agent-Planner-Executor structure.
- [x] Establish abstract `BaseTool` interface and registry.
- [x] Add slash command system.
- [x] Implement TOML configuration loader.
- [x] Implement interaction logging.

## Phase 3: Tools Integration (Next)
- [ ] Implement system tool definitions (e.g., ReadFileTool, WriteFileTool, RunCommandTool).
- [ ] Connect Planner reasoning capabilities to request tool calls from the LLM client.
- [ ] Implement safety prompts requesting user confirmation before tool execution.

## Phase 4: Local Memory Layer
- [ ] Incorporate simple SQLite file database or vector store for long-term memory.
- [ ] Store user preferences, projects, goals, and routines.
- [ ] Load and inject relevant memory facts dynamically based on conversation context.

## Phase 5: Automation & Proactivity
- [ ] Background monitoring utilities.
- [ ] Event-driven action suggestions (e.g., system diagnostics, file clutter organization warnings).
- [ ] Fully configurable scheduling settings.
