#! /usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "requests",
# ]
# ///

import argparse
import requests
import json
from nba.scoreboard import NBAScoreboard

URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description = "ESPN client for sports data")
    p.add_argument(
        "-wd",
        "--write-data",
        action = "store_true",
        help = "Write scoreboard data to disc",
    )
    p.add_argument(
        "-d",
        "--date",
        help = "Date to retrieve games for in (YYYYMMDD)"
    )
    return p.parse_args()

def fetch_nba_scoreboard(date: str | None = None) -> dict:
    params = {}
    if date:
        params["dates"] = date
    resp = requests.get(
        URL,
        headers = {"User-Agent": "nba-scores-learning-script/1.0"},
        params = params,
        timeout = 10,
    )
    resp.raise_for_status()
    return resp.json()

def write_scoreboard_data(data: dict):
    with open("../data/nba_scoreboard.json", "w") as file:
        json.dump(data, file, indent = 4)

def main() -> int:
   args = parse_args()
   data = fetch_nba_scoreboard(args.date)
   if args.write_data:
       write_scoreboard_data(data)

   scoreboard = NBAScoreboard.from_dict(data)
   scoreboard.print_games()

   return 0

if __name__ == "__main__":
    raise SystemExit(main())
