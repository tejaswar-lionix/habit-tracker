import unittest
from datetime import date

from habits import add_habit, check, streak


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


if __name__ == "__main__":
    unittest.main()
