# Implementation Plan: Backend API & Web UI

**Date**: 2026-06-27  
**Status**: Planning complete, implementation not yet started

---

## Overview

Extend the ESPN Scoreboard CLI into a full-stack web application with a FastAPI backend and a React frontend, while preserving the existing CLI as a fully functional standalone tool.

---

## Goals

- Expose scoreboard data via a REST API (FastAPI)
- Provide a browser-based scoreboard UI with live auto-refresh
- Keep the CLI (`uv run src/espn-scoreboard.py`) working without modification
- Run the full stack locally via a single `docker compose up` command

---

## Decisions & Reasoning

### Backend: FastAPI

**Decision**: Use FastAPI for the backend API layer.

**Reasoning**:
- The project is already Python — no new language or runtime needed
- Existing `dataclass` + `from_dict()` models translate naturally to Pydantic response models
- The existing fetch functions in `src/espn_client.py` are reusable as-is
- FastAPI generates OpenAPI/Swagger docs automatically, useful for debugging and agent-assisted frontend development
- Async-ready and performant for a simple read-only API use case
- Works seamlessly with `uv`

### Frontend: React + Vite + Tailwind CSS

**Decision**: Use React 18 with Vite as the build tool and Tailwind CSS for styling.

**Reasoning**:
- **React**: Best choice for agent-delegated frontend work — the most well-represented framework in agent training data, producing the most consistent and correct output
- **Vite**: Fast dev server, minimal config, standard pairing with React
- **Tailwind CSS**: Utility-first CSS is agent-friendly — styles are explicit and inline, requiring no context-switching between `.jsx` and `.css` files. Produces clean results for a card-based scoreboard layout with no design system overhead

CSS Modules were considered but ruled out — better suited for large teams with strict style separation requirements, unnecessary complexity for a personal local tool built primarily by agents.

### Unified Game Response Schema

**Decision**: Use a single unified `GameResponse` Pydantic model across all leagues, with optional fields for sport-specific data.

**Reasoning**:
- The frontend builds **one `GameCard` component** that conditionally renders optional sections — far simpler than per-league rendering paths
- Adding a new league in the future (e.g., NFL, NHL) only requires backend changes; the frontend picks it up automatically
- Optional fields (`series_info`, `status_detail`, `record`) map naturally to `null` in JSON and conditional rendering in React
- The existing CLI code already handles this implicitly — `series_data` is only printed when present

A per-league schema was considered but ruled out — it would require the agent-built frontend to maintain separate rendering logic per sport, increasing complexity and fragility over time.

### Polling Interval via `/config` Endpoint

**Decision**: The API exposes a `GET /config` endpoint that returns `poll_interval_ms`. The value is set via a `POLL_INTERVAL_MS` environment variable on the API container (default: 120000ms / 2 minutes).

**Reasoning**:
- The UI fetches config once on load — no hardcoded values, no rebuild needed to change the interval
- Environment variables are the idiomatic Docker way to configure services at startup
- Avoids the need for mounted config files or separate config management
- Changing the interval is a one-line change to `docker-compose.yml` followed by `docker compose up`

### Agent Strategy: Specialized Frontend Agent

**Decision**: Use a dedicated frontend coding agent (`.github/agents/espn-frontend.agent.md`) with explicit scope constraints rather than a generic agent.

**Reasoning**:
- A generic agent will modify files outside its intended scope when it perceives a need, breaking the intended backend/frontend separation
- Scope constraints (`ui/` only) prevent the agent from making unauthorized changes to `api/` or `src/`
- Explicit API contract documentation in the agent instructions removes ambiguity — the agent works from a known interface, not assumed behavior
- When a backend change is needed, the agent is instructed to open a GitHub issue rather than self-implement, maintaining a clean handoff back to the developer
- Frontend-specific conventions (React hooks only, no class components, Tailwind, `fetch` over axios) produce more consistent output than relying on agent defaults

---

## API Contract

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/config` | Returns app configuration (poll interval) |
| `GET` | `/leagues` | Returns list of supported leagues |
| `GET` | `/scoreboard` | Returns scoreboard for a league and optional date |

### Query Parameters — `/scoreboard`

| Param | Required | Format | Description |
|-------|----------|--------|-------------|
| `league` | Yes | `nba` \| `mlb` \| `wnba` \| `fifa` | League to fetch |
| `date` | No | `YYYYMMDD` | Specific date; defaults to today |

### Response Shapes

```json
// GET /config
{ "poll_interval_ms": 120000 }

// GET /leagues
{ "leagues": ["nba", "mlb", "wnba", "fifa"] }

// GET /scoreboard?league=nba
{
  "league": "nba",
  "date_display": "Today",
  "games": [
    {
      "name": "Cleveland Cavaliers at Detroit Pistons",
      "time": "07:00 PM",
      "status": "In Progress",
      "status_detail": "Q3 - 2:14",
      "away_team": { "name": "Cavaliers", "score": "74", "record": "52-30" },
      "home_team": { "name": "Pistons", "score": "68", "record": "44-38" },
      "series_info": "East Semifinals - Game 5 (2-2)",
      "stat_leaders": [
        { "label": "Points", "athlete_name": "D. Mitchell", "value": "22.0" },
        { "label": "Rebounds", "athlete_name": "E. Mobley", "value": "9.0" },
        { "label": "Assists", "athlete_name": "D. Garland", "value": "6.0" }
      ]
    }
  ]
}
```

**Optional fields** (may be `null`):
- `status_detail` — context-specific game clock/state for in-progress games
- `series_info` — only present during NBA/WNBA playoff series
- `record` on teams — not present for FIFA
- `stat_leaders` — may be empty for FIFA or pre-game

---

## Project Structure (Target)

```
espn-scoreboard/
├── .github/
│   ├── agents/
│   │   └── espn-frontend.agent.md   # Frontend coding agent instructions
│   ├── copilot-instructions.md       # Repo-wide Copilot instructions
│   └── CODEOWNERS
├── api/
│   ├── Dockerfile
│   ├── main.py                       # FastAPI app, CORS, all routes
│   └── models.py                     # Pydantic response models (API contract)
├── ui/
│   ├── Dockerfile
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── src/
│       ├── App.jsx
│       ├── index.css                 # Tailwind directives only
│       └── components/
│           ├── LeagueSelector.jsx
│           ├── Scoreboard.jsx
│           ├── GameCard.jsx
│           └── StatLeaders.jsx
├── src/                              # Original CLI — unchanged
├── data/
├── plans/
│   └── backend-api-and-ui.md         # This document
├── docker-compose.yml
└── pyproject.toml
```

---

## Implementation Tasks

### Phase 1 — Setup & Conventions

| Task | Description | Owner |
|------|-------------|-------|
| Create agent instructions | `.github/copilot-instructions.md` + `.github/agents/espn-frontend.agent.md` | ✅ Done |
| Create directory skeletons | `api/` and `ui/` top-level directories | You |

### Phase 2 — Backend (FastAPI)

*All backend tasks are manual — do not delegate to agents.*

| Task | Description | Depends On |
|------|-------------|------------|
| Define Pydantic models | `api/models.py` — unified `GameResponse`, `TeamResponse`, `StatLeaderResponse`, `ScoreboardResponse`, `ConfigResponse`, `LeaguesResponse` | Directory skeletons |
| FastAPI app skeleton | `api/main.py` — app init, CORS configured for `localhost:5173` | Directory skeletons |
| `GET /config` endpoint | Returns `poll_interval_ms` from `POLL_INTERVAL_MS` env var (default 120000) | App skeleton |
| `GET /leagues` endpoint | Returns `SUPPORTED_LEAGUES` from `src/espn_client.py` | App skeleton |
| `GET /scoreboard` endpoint | Accepts `league` + optional `date`; reuses fetch functions from `src/espn_client.py` | App skeleton + Pydantic models |
| Serialization layer | Map `NBAGame` / `MLBGame` / `WNBAGame` / `FIFAGame` → `GameResponse` | Pydantic models + scoreboard endpoint |
| API Dockerfile | Python 3.12 slim, `src/` on `PYTHONPATH`, uvicorn on port 8000 | Serialization layer |

### Phase 3 — Frontend (React + Vite)

*All frontend tasks are agent-delegated using `.github/agents/espn-frontend.agent.md`.*

| Task | Description | Depends On |
|------|-------------|------------|
| Scaffold Vite + React | Init project in `ui/`, configure Tailwind, set API proxy | Pydantic models (contract defined) |
| League selector + scoreboard components | `LeagueSelector`, `Scoreboard`, `GameCard`, `StatLeaders` | Scaffold |
| Auto-refresh polling | Fetch `/config` on load, `setInterval` re-fetch, last-updated timestamp | `/config` endpoint + scaffold |
| UI Dockerfile | Node 20, Vite dev server on port 5173, `VITE_API_BASE_URL` env var | Components + polling |

### Phase 4 — Docker Compose

| Task | Description | Depends On |
|------|-------------|------------|
| `docker-compose.yml` | Wire `api` (8000) + `ui` (5173), pass `POLL_INTERVAL_MS` to api | Both Dockerfiles |
| End-to-end smoke test | `docker compose up`, verify UI, dropdown, scoreboard, polling. Confirm CLI still works. | docker-compose.yml |

---

## Out of Scope (This Plan)

- `--write-data` path bug in `src/espn_client.py` — deferred to a separate task
- Authentication or multi-user support
- Production deployment (nginx, HTTPS, hosted infrastructure)
- Additional sports (NFL, NHL, etc.) — follow the "Adding a New Sport" guide in README
