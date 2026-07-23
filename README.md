# ESPN Scoreboard

A command-line tool and web application that fetches and displays live sports scoreboard data from the ESPN public API. Supports NBA, MLB, WNBA, and FIFA (soccer).

## Features

- Fetches live scoreboard data from the ESPN public API for NBA, MLB, WNBA, and FIFA
- Displays games for today or a specified date with scores and game status (Central Time)
- Shows per-game statistical leaders for points, rebounds, and assists (NBA/WNBA), and batting stats (MLB)
- Select any supported league via the `--league` flag
- Optionally writes raw API response data to disk for inspection or development
- **FastAPI backend** that exposes scoreboard data as JSON for web clients
- **Dockerized API** for containerized deployment

## Project Structure

```
espn-scoreboard/
├── pyproject.toml
├── api/
│   ├── Dockerfile                  # Docker image for the FastAPI backend
│   ├── main.py                     # FastAPI app — routes and CORS config
│   ├── models.py                   # Pydantic response models
│   └── serializers.py              # Converts domain objects to API responses
├── bin/
│   ├── build-api                   # Builds the Docker image for the API
│   ├── run-api                     # Runs the FastAPI dev server locally
│   └── run-api-docker              # Runs the API in a Docker container
├── data/
│   ├── nba_scoreboard.json         # Raw API response (written with --write-data)
│   ├── mlb_scoreboard.json
│   ├── wnba_scoreboard.json
│   └── fifa_scoreboard.json
└── src/
    ├── espn-scoreboard.py          # Entry point and CLI
    ├── espn_client.py              # League routing, URL constants, fetch logic
    ├── base.py                     # Abstract base classes: Scoreboard, Game, Team, StatLeader
    ├── exceptions.py               # Custom exceptions (UnsupportedLeagueError, etc.)
    ├── nba/
    │   ├── scoreboard.py           # NBAScoreboard: top-level container for all games
    │   ├── game.py                 # NBAGame: game details, scores, stat leader lookups
    │   ├── team.py                 # NBATeam: team info, score, and per-team leaders
    │   └── stat_leader.py          # StatLeader: individual stat leader data and comparison
    ├── mlb/
    │   ├── scoreboard.py           # MLBScoreboard
    │   ├── game.py                 # MLBGame
    │   ├── team.py                 # MLBTeam
    │   └── stat_leader.py          # StatLeader (batting: RBI, HR, AVG)
    ├── wnba/
    │   ├── scoreboard.py           # WNBAScoreboard
    │   ├── game.py                 # WNBAGame: game details, scores, series info, stat leaders
    │   ├── team.py                 # WNBATeam
    │   └── stat_leader.py          # StatLeader (points, rebounds, assists)
    ├── fifa/
    │   ├── scoreboard.py           # FIFAScoreboard
    │   └── game.py                 # FIFAGame: match details, score, clock
    └── utils/
        └── date.py                 # Shared date/time helpers (Central Time conversion)
```

## Requirements

- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) for dependency management and running scripts
- Docker (optional, for containerized API)

## Running the CLI

### With `uv` (recommended)

The script uses inline script dependencies and can be run directly with `uv`:

```bash
uv run src/espn-scoreboard.py
```

### Optional Flags

| Flag | Description |
|------|-------------|
| `-wd` / `--write-data` | Write the raw ESPN API response to `data/<league>_scoreboard.json` |
| `-l` / `--league` | League to display (`nba`, `mlb`, `wnba`, `fifa`). Defaults to `nba` |
| `-d` / `--date` | Date to retrieve games for in `YYYYMMDD` format. Defaults to today |

```bash
# Write raw data to disk
uv run src/espn-scoreboard.py --write-data

# View WNBA scoreboard
uv run src/espn-scoreboard.py --league wnba

# View FIFA matches for a specific date
uv run src/espn-scoreboard.py -l fifa -d 20250701
```

## Example Output (NBA)

```
1 Game Today

Cleveland Cavaliers at Detroit Pistons (10:44 - 2nd Quarter)
East Semifinals - Game 5 (2-2)
Time: 07:00 PM
Current Score: Cavaliers(52-30) 30 - Pistons(60-22) 34
Leaders:
  Points: C. Cunningham, 15.0
  Rebounds: E. Mobley, 7.0
  Assists: D. Garland, 4.0
```

## Example Output (MLB)

```
13 Games Today

Colorado Rockies at Los Angeles Dodgers (Final)
Time: 8:10 PM
Score: Rockies 0 - Dodgers 0
Leaders:
  Runs Batted In: Brandon Lowe, 1.0
  Home Runs: Henry Davis, 1.0
  Batting Average: Spencer Horwitz, 0.667
```

## Example Output (WNBA)

```
3 Games Today

Las Vegas Aces at New York Liberty (Final)
WNBA Finals - Game 3 (2-0)
Time: 07:30 PM
Final Score: Aces(28) 85 - Liberty(30) 91
Leaders:
  Points: B. Stewart, 26.0
  Rebounds: B. Stewart, 9.0
  Assists: S. Ionescu, 7.0
```

## Example Output (FIFA)

```
2 Games Today

USA vs Portugal (In Progress)
Time: 02:00 PM
Score: USA 1 - Portugal 0 (45:00)

Brazil vs Argentina (Final)
Time: 11:00 AM
Score: Brazil 2 - Argentina 2 (90:00)
```

## FastAPI Backend

The `api/` directory contains a FastAPI application that serves scoreboard data as JSON. It reuses the fetch and parsing logic from `src/espn_client.py` — the CLI remains fully independent.

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/leagues` | Returns the list of supported league identifiers |
| `GET` | `/config` | Returns runtime configuration (e.g., poll interval) |
| `GET` | `/scoreboard` | Returns scoreboard data for a given league and optional date |

**`GET /scoreboard` query parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `league` | Yes | League identifier: `nba`, `mlb`, `wnba`, `fifa` |
| `date` | No | Date in `YYYYMMDD` format. Defaults to today |

### Running the API Locally

Install dependencies and start the dev server:

```bash
uv sync
bin/run-api
```

The API will be available at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/docs`.

### Running the API with Docker

```bash
# Build the image
bin/build-api

# Run the container
bin/run-api-docker
```

The container exposes port `8000`. The `POLL_INTERVAL_MS` environment variable controls the client poll interval (default: `120000`ms).

## Architecture Overview

The codebase is organized around a simple parsing pipeline:

1. **CLI** — `espn-scoreboard.py` parses arguments and builds a `ClientConfig`.
2. **Route** — `espn_client.py` dispatches to the correct fetch function based on `--league` and calls the appropriate `Scoreboard.from_dict()`.
3. **Parse** — Each sport's `Scoreboard.from_dict()` walks the response, constructing `Game` and (where applicable) `Team` objects.
4. **Enrich** — Each `Team` holds a list of `StatLeader` objects parsed from the `leaders` field (NBA, MLB, WNBA).
5. **Display** — `scoreboard.print_games()` renders a formatted summary to stdout.

The FastAPI backend (`api/`) sits alongside the CLI and reuses steps 2–4:

1. **Route** — `main.py` receives HTTP requests and delegates to `espn_client.fetch_espn_data()`.
2. **Serialize** — `serializers.py` maps domain dataclasses to Pydantic response models defined in `models.py`.
3. **Respond** — FastAPI serializes the Pydantic models to JSON.

Each domain layer is a plain Python `dataclass` with a `from_dict()` class method. FIFA follows a simplified version of this pattern (no team-level stat leaders). Shared date/time logic lives in `utils/date.py`.

## Adding a New Sport

To add support for a new sport (e.g., NFL, NHL):

1. Create a new package under `src/` (e.g., `src/nfl/`).
2. Implement the same `dataclass` + `from_dict()` pattern used in the existing sports packages.
3. Add a new URL constant and fetch function in `espn_client.py`.
4. Add the league name to `SUPPORTED_LEAGUES` and wire it into the `match` block in `fetch_espn_data()`.
5. If the sport has unique stat categories, verify the `serializers.py` mapping handles them correctly.

The ESPN API follows a consistent URL pattern:
```
https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard
```

## Implementation Plans

Detailed plans for larger features — including decisions, reasoning, API contracts, and task breakdowns.

| Plan | Description | Status |
|------|-------------|--------|
| [Backend API & Web UI](plans/backend-api-and-ui.md) | Add FastAPI backend + React/Vite frontend with Docker Compose, while preserving the CLI | API complete; UI in progress |

## Roadmap

See [TASKS.md](TASKS.md) for planned features and improvements.

## Data Source

All data is fetched from the [ESPN public API](https://www.espn.com). This is an unofficial, unauthenticated endpoint intended for personal and educational use.
