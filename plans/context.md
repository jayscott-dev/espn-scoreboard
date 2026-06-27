# Project Context

> **Purpose**: Quick orientation for planning sessions, implementation handoffs, and agent tasking.  
> **Update this file** when major decisions change or new phases are completed.

---

## What This Project Is

A Python CLI tool that fetches and displays live ESPN scoreboard data for NBA, MLB, WNBA, and FIFA.
Being extended to include a FastAPI backend and React web UI, while keeping the CLI fully functional.

---

## Current State

| Layer | Status | Notes |
|-------|--------|-------|
| CLI (`src/`) | ✅ Complete | `uv run src/espn-scoreboard.py` — do not break this |
| FastAPI backend (`api/`) | 🔲 Not started | See `plans/backend-api-and-ui.md` |
| React UI (`ui/`) | 🔲 Not started | Agent-delegated, see agent instructions below |
| Docker Compose | 🔲 Not started | Target: single `docker compose up` |

---

## Tech Stack

| Concern | Choice | Why |
|---------|--------|-----|
| CLI runtime | Python 3.12 + `uv` | Existing — unchanged |
| Backend API | FastAPI + uvicorn | Python-native, Pydantic models, auto OpenAPI docs |
| Frontend | React 18 + Vite | Best agent output quality; most represented in training data |
| Styling | Tailwind CSS | Utility-first, agent-friendly, no context-switching between files |
| Orchestration | Docker Compose | Single-command local startup |

---

## Key Architectural Decisions

### Unified Game Schema
All leagues (`nba`, `mlb`, `wnba`, `fifa`) return the same `GameResponse` shape from the API.
Sport-specific fields (`series_info`, `status_detail`, team `record`) are optional/nullable.
- **Why**: One frontend component handles all leagues; adding a new sport requires no frontend changes.

### CLI Preserved As-Is
`src/` is never modified by API or UI work. The API reuses fetch functions from `src/espn_client.py`
but does not alter the CLI entry point or any existing models.

### Poll Interval via `/config` Endpoint
The UI fetches `GET /config` on load to get `poll_interval_ms` (default: 120000ms / 2 min).
Configured via `POLL_INTERVAL_MS` env var on the API container — no UI rebuild needed to change it.

### Agent Strategy
Frontend is built by a dedicated coding agent scoped to `ui/` only.
- Agent file: `.github/agents/espn-frontend.agent.md`
- If backend work is needed, agent opens a GitHub issue — does not self-implement
- Repo-wide conventions: `.github/copilot-instructions.md`

---

## API Contract (Quick Reference)

```
GET /config        → { poll_interval_ms: 120000 }
GET /leagues       → { leagues: ["nba", "mlb", "wnba", "fifa"] }
GET /scoreboard    → ScoreboardResponse (see below)
  ?league=nba      (required)
  &date=YYYYMMDD   (optional, defaults to today)
```

**Unified `GameResponse` fields:**

| Field | Type | Optional? |
|-------|------|-----------|
| `name` | string | No |
| `time` | string (CT) | No |
| `status` | string | No |
| `status_detail` | string | Yes — in-progress clock/state |
| `away_team` / `home_team` | TeamResponse | No |
| `team.record` | string | Yes — absent for FIFA |
| `series_info` | string | Yes — NBA/WNBA playoffs only |
| `stat_leaders` | StatLeaderResponse[] | No — may be empty |

Full contract with example responses: [`plans/backend-api-and-ui.md`](backend-api-and-ui.md)

---

## Running the Project

```bash
# CLI (always works independently)
uv run src/espn-scoreboard.py --league nba

# Full stack (once implemented)
docker compose up
# UI → http://localhost:5173
# API → http://localhost:8000
```

---

## Key Files

| File | Purpose |
|------|---------|
| `src/espn_client.py` | League routing, ESPN fetch functions, `SUPPORTED_LEAGUES` |
| `src/utils/date.py` | Central Time conversion helpers |
| `api/models.py` | Pydantic response models (API contract) |
| `api/main.py` | FastAPI app, all routes |
| `.github/agents/espn-frontend.agent.md` | Frontend agent scope + instructions |
| `.github/copilot-instructions.md` | Repo-wide Copilot conventions |
| `plans/backend-api-and-ui.md` | Full implementation plan with decisions |

---

## Open Deferred Items

- `--write-data` flag uses a relative path (`../data/`) that breaks if not run from `src/` — fix deferred
