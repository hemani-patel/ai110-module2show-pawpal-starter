# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps a pet owner plan daily care tasks for their pets.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

## Features

- **Add pets** — Register pets with name, species, and age.
- **Schedule tasks** — Create care tasks with a time, duration, priority, and frequency (once / daily / weekly).
- **Sorted daily schedule** — View all of today's tasks in chronological order.
- **Filter by pet or status** — Narrow the schedule to one pet, or show only pending/completed tasks.
- **Conflict warnings** — Get an alert when two tasks are booked at the same time.
- **Recurring tasks** — Daily and weekly tasks automatically generate their next occurrence when marked complete.
- **Mark tasks complete** — Check off tasks from the UI and see updated status.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
python3 -m streamlit run app.py
```

### Run the CLI demo

```bash
python3 main.py
```

## Smarter Scheduling

The `Scheduler` class provides four algorithmic features:

- **Sort by time** — Tasks are sorted by their `HH:MM` time string so the daily schedule reads in chronological order.
- **Filter by pet or status** — View only one pet's tasks, or only pending/completed tasks.
- **Conflict detection** — If two tasks are scheduled at the exact same time, the scheduler returns a warning message for each conflict.
- **Recurring tasks** — When a daily or weekly task is marked complete, a new task is automatically created for the next occurrence (tomorrow for daily, +7 days for weekly).

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

The suite includes 10 tests covering:

- **Task basics** — marking complete, adding tasks to a pet
- **Sorting** — tasks come back in chronological order
- **Recurrence** — daily tasks create a next-day copy, weekly tasks create a next-week copy, one-time tasks don't recur
- **Conflict detection** — same-time tasks produce warnings, different-time tasks produce none
- **Edge cases** — pet with no tasks returns an empty schedule, looking up a non-existent pet returns None

**Confidence level:** 4/5 stars. All core behaviors are tested. The main gap is duration-based overlap detection, which the scheduler intentionally doesn't implement.
