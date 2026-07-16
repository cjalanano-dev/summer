# Changelog

All notable changes to Project Summer will be documented in this file.

## [0.3.0] - 2026-07-17
### Added
- Created unified `ToolRegistry` (replacing the old `ToolManager`) to register and dispatch `BaseTool` instances.
- Implemented 5 safe, isolated tool plugins: Calculator, Current Time, Random Number, UUID Generator, and Password Generator.
- Implemented 2 system tools: System Info and Directory List Explorer.
- Refactored Agent execution loops (`Planner`, `Executor`, and `Agent`) to support rule-based tool routing, execution dispatch, and context notice injection.

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
