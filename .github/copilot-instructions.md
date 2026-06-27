# ESPN Scoreboard — Copilot Instructions

## Project Overview

A Python CLI tool and web application that fetches live sports scoreboard data from the ESPN public API.
Supports NBA, MLB, WNBA, and FIFA.

## Repository Structure

```
espn-scoreboard/
├── src/              # Existing CLI — Python dataclasses + ESPN fetch logic
├── api/              # FastAPI backend — exposes scoreboard data as JSON
├── ui/               # React + Vite frontend — scoreboard display
├── data/             # Raw ESPN API responses (written with --write-data flag)
└── docker-compose.yml
```

## Critical Rule: CLI Must Always Work

The `src/` directory contains the original CLI application. It must remain fully functional.
**Never modify `src/` files unless the task explicitly targets the CLI.**
The API reuses fetch logic from `src/espn_client.py` — do not break that interface.

## Language & Runtime

- **Backend**: Python 3.12+, managed with `uv`
- **Frontend**: React 18+, Vite, Node 20+
- **Orchestration**: Docker Compose

## Python Conventions

- Use `@dataclass` with `@classmethod from_dict()` for all data models
- Use type hints on all function signatures
- Prefer `match` statements over long `if/elif` chains for league dispatch
- Only comment code that needs clarification — no obvious comments
