#!/usr/bin/env python3
"""Track simple daily habits and compute streaks."""
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


def weekly_summary(habits, today=None):
    """Count checks per habit in the seven days ending today."""
    today = today or date.today()
    window = {(today - timedelta(days=offset)).isoformat() for offset in range(7)}
    return {
        habit["name"]: len(window.intersection(habit["checks"]))
        for habit in habits
    }
