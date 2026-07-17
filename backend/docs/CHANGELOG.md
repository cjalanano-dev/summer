# Changelog

All notable changes to Project Summer will be documented in this file.

## [0.5.0] - 2026-07-17
### Added
- Created decoupled workspace context analysis package (`app/workspace/` containing `models`, `detector`, `scanner`, `analyzer`, and `manager`).
- Implemented upward parent directory traversal to detect root indicators (like `.git`, `pyproject.toml`, `package.json`).
- Implemented noise-filtering recursive workspace scanning with total byte size calculations.
- Implemented extension frequency analysis and rule-based language stack classification (mapping pyproject.toml, package.json, Cargo.toml, pom.xml, go.mod, build.gradle, CMakeLists.txt, Makefile).
- Implemented important file discovery mapping configurations, readmes, and scripts.
- Implemented cached workspace manager context with `refresh()` and `summary()` formatter APIs.
- Implemented active directory change tracking inside `get_workspace()` caching logic.
- Implemented automated prompt context injection appending project metadata to LLM dialogue threads.
- Added `/refresh-workspace` CLI slash command to trigger manual project updates.
- Implemented `WorkspaceSummaryTool` allowing the LLM planner to autonomously query project structure via tool call without knowing the underlying workspace internals.

## [0.4.1] - 2026-07-17
### Added
- Implemented `ReadFileTool` with workspace restriction, 1MB size threshold limits, and binary checks.
- Implemented `SearchFilesTool` utilizing glob patterns with `.venv` directories filtering for noise reduction.
- Implemented `ReadMultipleFilesTool` to retrieve content batches.
- Implemented `ClipboardTool` utilizing `pyperclip` to support clipboard gets, sets, and clears.

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
