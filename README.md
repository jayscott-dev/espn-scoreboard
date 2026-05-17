# ESPN Scoreboard

A command-line tool that fetches and displays live sports scoreboard data from the ESPN public API. Currently supports NBA, with plans to expand to additional sports.

## Features

- Fetches live NBA scoreboard data from the ESPN public API
- Displays today's games with scores, game status, and tip-off times (Central Time)
- Shows per-game statistical leaders for points, rebounds, and assists
- Optionally writes raw API response data to disk for inspection or development

## Project Structure

```
espn-scoreboard/
├── pyproject.toml
├── data/
│   └── nba_scoreboard.json       # Raw API response (written with --write-data)
└── src/
    ├── espn-scoreboard.py         # Entry point and CLI
    └── nba/
        ├── scoreboard.py          # NBAScoreboard: top-level container for all games
        ├── game.py                # NBAGame: game details, scores, stat leader lookups
        ├── team.py                # NBATeam: team info, score, and per-team leaders
        └── stat_leader.py         # StatLeader: individual stat leader data and comparison
```

## Requirements

- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip`

## Running the Script

### With `uv` (recommended)

The script uses inline script dependencies and can be run directly with `uv`:

```bash
uv run src/espn-scoreboard.py
```

### Optional Flags

| Flag | Description |
|------|-------------|
| `-wd` / `--write-data` | Write the raw ESPN API response to `data/nba_scoreboard.json` |

```bash
uv run src/espn-scoreboard.py --write-data
```

## Example Output

```
1 Game Today

Cleveland Cavaliers at Detroit Pistons (10:44 - 2nd Quarter)
East Semifinals - Game 5
Time: 07:00 PM
Current Score: Cavaliers(52-30) 30 - Pistons(60-22) 34
Overall Points Leader: C. Cunningham, 15.0
Overall Rebounds Leader: A. Thompson, 4.0
Overall Assists Leader: A. Thompson, 4.0
```

## Architecture Overview

The codebase is organized around a simple parsing pipeline:

1. **Fetch** — `espn-scoreboard.py` calls the ESPN public API and gets a raw JSON response.
2. **Parse** — `NBAScoreboard.from_dict()` walks the response, constructing `NBAGame` and `NBATeam` objects.
3. **Enrich** — Each `NBATeam` holds a list of `StatLeader` objects parsed from the `leaders` field.
4. **Display** — `scoreboard.print_games()` renders a formatted summary to stdout.

Each layer is a plain Python `dataclass` with a `from_dict()` class method, making it straightforward to add new sports by following the same pattern.

## Adding a New Sport

To add support for a new sport (e.g., NFL, MLB, NHL):

1. Create a new package under `src/` (e.g., `src/nfl/`).
2. Implement the same `dataclass` + `from_dict()` pattern used in `src/nba/`.
3. Add a new fetch function and URL constant in `espn-scoreboard.py`.
4. Wire up a new CLI argument or sub-command to select the sport.

The ESPN API follows a consistent URL pattern:
```
https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard
```

## Roadmap

See [TASKS.md](TASKS.md) for planned features and improvements.

## Data Source

All data is fetched from the [ESPN public API](https://www.espn.com). This is an unofficial, unauthenticated endpoint intended for personal and educational use.
