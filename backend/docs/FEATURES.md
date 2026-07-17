# Project Summer Features

This document describes Summer's active and planned capabilities.

## Current Features (Phase 2)

- **Interactive Shell Session**: Start interactive conversations via `summer`.
- **Slash Commands**: Intercept commands locally (`/help`, `/clear`, `/history`, `/model`, `/config`, `/about`, `/exit`).
- **TOML Configurations**: Configure parameters via `config.toml` (default model, temperature, theme, stream, system prompt path).
- **Persistent Interaction Logging**: Every user prompt and assistant response is stored in `logs/summer.log` with timestamps.
- **Model Switcher**: Manage local Ollama model settings interactively via table lists.

## Planned Features

- **File System Tools**: Safely view, edit, search, and list local workspace files.
- **Shell Integrations**: Execute local command-line operations (always prompting for confirmation).
- **Local Memory**: Retain user preferences, projects, goals, and routines.
- **Task Organization**: Schedule notifications and manage daily Todo items.
