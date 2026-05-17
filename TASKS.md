# Tasks

Planned features and improvements for the ESPN Scoreboard project.

## Backlog

- [ ] Probability of winning based off record
- [ ] Reduce complexity around `StatLeader`
- [ ] Add team to `StatLeader`
- [ ] Optionally restrict `StatLeader`s by stat type
- [ ] Retrieve games by date

## Done

- [x] Display game in series (e.g., "Game 3 of 7")
- [x] Display quarter for games (events, competitions, status '1024')
    - "(Scheduled)" if not started
    - "(Final)" if game over
    - "(Q3 - 1:56)" if in progress (quarter and time remaining)
- [x] Update Game terminology in display (Games vs Game for only 1 game)
- [x] Display records for each team (e.g., "48-34")