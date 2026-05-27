# Tasks

Planned features and improvements for the ESPN Scoreboard project.

## Backlog



## MLB Backlog

- [ ] Add current inning to game title
- [ ] Current outs to game title
- [ ] Print date for -d instead of saying Games Today

## Done

- [x] Display game in series (e.g., "Game 3 of 7")
- [x] Display quarter for games (events, competitions, status '1024')
    - "(Scheduled)" if not started
    - "(Final)" if game over
    - "(Q3 - 1:56)" if in progress (quarter and time remaining)
- [x] Update Game terminology in display (Games vs Game for only 1 game)
- [x] Display records for each team (e.g., "48-34")
- [x] Retrieve games by date
- [x] Add series record: Game 7 (3-3)
- [x] Reduce complexity around `StatLeader`
- [x] Put convert_date in its own spot
- [x] Data structure for espn_client