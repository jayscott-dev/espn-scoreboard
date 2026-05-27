#! /usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "requests",
# ]
# ///

import argparse
import espn_client as ec 

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
        help = "Date to retrieve games for in (YYYYMMDD)",
    )
    p.add_argument(
        "-l",
        "--league",
        help = "League to view scoreboard for",
        default = "nba",
        choices = ec.SUPPORTED_LEAGUES
    )
    return p.parse_args()

def main() -> int:
   args = parse_args()
   client_config = ec.ClientConfig (
       league = args.league,
       write_data = args.write_data,
       date = args.date,
   )

   ec.fetch_espn_data(client_config)

   return 0

if __name__ == "__main__":
    raise SystemExit(main())
