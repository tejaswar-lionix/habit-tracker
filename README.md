# habit-tracker

Track daily habits and measure streaks.

## Usage

```bash
python3 -c "from datetime import date; from habits import *; h=add_habit([], 'read'); check(h, 'read', date.today()); print(streak(h, 'read'))"
python3 -c "from habits import *; h=add_habit([], 'read'); print(longest_streak(h, 'read'))"
python3 -c "from habits import *; h=add_habit(add_habit([], 'read'), 'run'); print(remove_habit(h, 'read'))"
python3 -c "from habits import *; export_history(add_habit([], 'read'), 'history.csv')"
```

## Features

- Add habits and check them once per day
- Remove habits by name with remove_habit(habits, name)
- Rename habits in place with rename_habit(habits, old, new)
- Consecutive-day streak calculation
- Longest run of consecutive days with longest_streak(habits, name)
- Seven-day summary with weekly_summary(habits)
- CSV history export with export_history(habits, path)

## Tests

```bash
python3 -m unittest -q
```

## License

MIT
