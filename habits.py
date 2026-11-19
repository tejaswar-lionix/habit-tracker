#!/usr/bin/env python3
"""Track simple daily habits and compute streaks."""
import csv
import json
import os
from datetime import date, timedelta

DEFAULT_PATH = os.path.expanduser("~/.habits.json")


def load(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def save(path, habits):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(habits, handle, indent=2)


def add_habit(habits, name):
    name = name.strip()
    if not name:
        raise ValueError("habit name must not be empty")
    habits.append({"name": name, "checks": []})
    return habits


def _find(habits, name):
    for habit in habits:
        if habit["name"] == name:
            return habit
    raise KeyError(f"unknown habit: {name}")


def remove_habit(habits, name):
    habit = _find(habits, name)
    habits.remove(habit)
    return habits


def rename_habit(habits, old, new):
    new = new.strip()
    if not new:
        raise ValueError("habit name must not be empty")
    habit = _find(habits, old)
    if new != old and any(other["name"] == new for other in habits):
        raise ValueError(f"habit already exists: {new}")
    habit["name"] = new
    return habits


def check(habits, name, day=None):
    habit = _find(habits, name)
    stamp = (day or date.today()).isoformat()
    if stamp not in habit["checks"]:
        habit["checks"].append(stamp)
    return habits


def streak(habits, name, today=None):
    habit = _find(habits, name)
    checked = set(habit["checks"])
    cursor = today or date.today()
    count = 0
    while cursor.isoformat() in checked:
        count += 1
        cursor -= timedelta(days=1)
    return count


def longest_streak(habits, name):
    habit = _find(habits, name)
    days = sorted({date.fromisoformat(stamp) for stamp in habit["checks"]})
    longest = 0
    current = 0
    previous = None
    for day in days:
        if previous is not None and day - previous == timedelta(days=1):
            current += 1
        else:
            current = 1
        longest = max(longest, current)
        previous = day
    return longest


def weekly_summary(habits, today=None):
    """Count checks per habit in the seven days ending today."""
    today = today or date.today()
    window = {(today - timedelta(days=offset)).isoformat() for offset in range(7)}
    return {
        habit["name"]: len(window.intersection(habit["checks"]))
        for habit in habits
    }


def export_history(habits, path):
    rows = []
    for habit in habits:
        for day in habit["checks"]:
            rows.append((habit["name"], day))
    rows.sort(key=lambda row: (row[1], row[0]))
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["habit", "date"])
        writer.writerows(rows)
    return path
