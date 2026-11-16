# habit-tracker

Track daily habits and measure streaks.

## Usage

```bash
python3 -c "from datetime import date; from habits import *; h=add_habit([], 'read'); check(h, 'read', date.today()); print(streak(h, 'read'))"
python3 -c "from habits import *; export_history(add_habit([], 'read'), 'history.csv')"
```

## Features

- Add habits and check them once per day
- Consecutive-day streak calculation
- Seven-day summary with weekly_summary(habits)
- CSV history export with export_history(habits, path)

## Tests

```bash
python3 -m unittest -q
```

## License

MIT
