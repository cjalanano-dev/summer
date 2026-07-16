# Changelog

All notable changes to Project Summer will be documented in this file.

## [0.4.0] - 2026-07-17
### Added
- Created SQLite structured key-value memory engine package (`app/memory/` containing `models`, `storage`, `retrieval`, and `manager`) storing records inside `data/summer.db`.
- Expanded `MemoryManager` API to support full programmatic CRUD controls: `remember()`, `forget()`, `update()`, `search()`, `get()`, `list()`, and `retrieve_context()`.
- Implemented background automatic memory extraction analyzing chat dialogue turns and storing key-value pairs silently.
- Implemented predefined categories (preference, person, project, goal, fact, routine, reminder, custom) with unique key constraints for automatic upserts.
- Refactored retrieval matching to boost and prioritize project records, top 5 preferences, and top 5 goals.
- Expanded forgetting routines to delete by ID, category, or key.
- Refactored `/memory` command to print category-grouped records.
- Added `/remember <category> <key> = <value>`, `/forget`, `/search-memory <q>`, and `/clear-memory` CLI slash commands.

## [0.3.0] - 2026-07-17
### Added
- Created unified `ToolRegistry` (replacing the old `ToolManager`) to register and dispatch `BaseTool` instances.
- Implemented 5 safe, isolated tool plugins: Calculator, Current Time, Random Number, UUID Generator, and Password Generator.
- Implemented 2 system tools: System Info and Directory List Explorer.
- Refactored Agent execution loops (`Planner`, `Executor`, and `Agent`) to support LLM-driven tool selection, structured JSON planning, execution dispatch, and context notice injection.

## [0.2.0] - 2026-07-16
### Added
- Created unified `Summer` coordinator class.
- Extracted `Conversation` history with JSON save/load capability.
- Established object-oriented `BaseTool` abstract interface.
- Intercepted console input with local slash commands (`/help`, `/clear`, `/history`, `/model`, `/config`, `/about`, `/exit`).
- Added TOML configuration loader parsing `config.toml` via `tomllib`.
- Added persistent interaction logging to `logs/summer.log` with timestamps.

## [0.1.0] - 2026-07-16
### Added
- Initial project layout.
- Command-line interface with Typer.
- Streaming responses from Ollama LLM.
- Model selector command storing configuration in `.env`.
