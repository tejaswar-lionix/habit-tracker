import csv
import os
import tempfile
import unittest
from datetime import date

from habits import add_habit, check, export_history, longest_streak, streak


class HabitTests(unittest.TestCase):
    def test_add_habit(self):
        habits = add_habit([], "read")
        self.assertEqual(habits[0]["name"], "read")
        self.assertEqual(habits[0]["checks"], [])

    def test_add_habit_rejects_blank_name(self):
        with self.assertRaises(ValueError):
            add_habit([], "  ")

    def test_check_is_idempotent_per_day(self):
        habits = add_habit([], "run")
        check(habits, "run", date(2026, 11, 10))
        check(habits, "run", date(2026, 11, 10))
        self.assertEqual(len(habits[0]["checks"]), 1)

    def test_streak_counts_consecutive_days(self):
        habits = add_habit([], "read")
        for day in (8, 9, 10):
            check(habits, "read", date(2026, 11, day))
        self.assertEqual(streak(habits, "read", date(2026, 11, 10)), 3)

    def test_streak_stops_at_gap(self):
        habits = add_habit([], "read")
        for day in (8, 10):
            check(habits, "read", date(2026, 11, day))
        self.assertEqual(streak(habits, "read", date(2026, 11, 10)), 1)

    def test_unknown_habit_raises(self):
        with self.assertRaises(KeyError):
            check([], "swim")


class LongestStreakTests(unittest.TestCase):
    def test_single_run(self):
        habits = add_habit([], "read")
        for day in (8, 9, 10):
            check(habits, "read", date(2026, 11, day))
        self.assertEqual(longest_streak(habits, "read"), 3)

    def test_gap_separated_runs_returns_longest(self):
        habits = add_habit([], "read")
        for day in (1, 2, 3, 6, 7):
            check(habits, "read", date(2026, 11, day))
        self.assertEqual(longest_streak(habits, "read"), 3)

    def test_empty_checks_returns_zero(self):
        habits = add_habit([], "read")
        self.assertEqual(longest_streak(habits, "read"), 0)

    def test_unknown_habit_raises(self):
        with self.assertRaises(KeyError):
            longest_streak([], "swim")


class ExportHistoryTests(unittest.TestCase):
    def test_rows_written_correctly(self):
        habits = add_habit([], "read")
        check(habits, "read", date(2026, 11, 10))
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "history.csv")
            result = export_history(habits, path)
            with open(path, encoding="utf-8") as handle:
                rows = list(csv.reader(handle))
        self.assertEqual(result, path)
        self.assertEqual(rows, [["habit", "date"], ["read", "2026-11-10"]])

    def test_multiple_habits_and_dates_sorted(self):
        habits = add_habit(add_habit([], "read"), "run")
        check(habits, "run", date(2026, 11, 11))
        check(habits, "read", date(2026, 11, 10))
        check(habits, "read", date(2026, 11, 11))
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "history.csv")
            export_history(habits, path)
            with open(path, encoding="utf-8") as handle:
                rows = list(csv.reader(handle))
        self.assertEqual(
            rows,
            [
                ["habit", "date"],
                ["read", "2026-11-10"],
                ["read", "2026-11-11"],
                ["run", "2026-11-11"],
            ],
        )

    def test_empty_habits_writes_header_only(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "history.csv")
            export_history([], path)
            with open(path, encoding="utf-8") as handle:
                rows = list(csv.reader(handle))
        self.assertEqual(rows, [["habit", "date"]])


class WeeklySummaryTests(unittest.TestCase):
    def test_weekly_summary_counts_last_seven_days(self):
        from habits import weekly_summary

        habits = add_habit(add_habit([], "read"), "run")
        for day in (4, 5, 10, 11):
            check(habits, "read", date(2026, 11, day))
        check(habits, "run", date(2026, 11, 11))
        summary = weekly_summary(habits, date(2026, 11, 11))
        self.assertEqual(summary, {"read": 3, "run": 1})


if __name__ == "__main__":
    unittest.main()
