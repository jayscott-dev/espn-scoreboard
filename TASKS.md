# Tasks

Planned features and improvements for the ESPN Scoreboard project.

## Backlog

- [ ] Writing data expects to be in src directory

## MLB Backlog

- [ ] Refine the RBI to have (4-4) at the end

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
- [x] Print date for -d instead of saying Games Today
     - Compare dates from first and last events
     - Dates are in UTC, convert to Central
     - If dates are different, say "from {date} to {date}"
     - If dates are the same, use single date
     - If single date, check to see if it is today
     - If today, print "Today"
- [x] Add current inning to game title
- [x] Current outs to game title