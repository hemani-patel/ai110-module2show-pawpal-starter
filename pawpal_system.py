from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
    """A single pet care activity."""
    description: str
    time: str  # "HH:MM" format
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    frequency: str  # "once", "daily", "weekly"
    pet_name: str
    completed: bool = False
    date: date = field(default_factory=date.today)

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    """A pet with its basic info and associated care tasks."""
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, description: str):
        """Remove a task by its description."""
        self.tasks = [t for t in self.tasks if t.description != description]

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return self.tasks


class Owner:
    """A pet owner who manages one or more pets."""

    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        """Register a new pet under this owner."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Retrieve a pet by name, or None if not found."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_all_tasks(self) -> list[Task]:
        """Collect every task from every pet into a single list."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Organises and manages tasks across all of an owner's pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_daily_schedule(self, target_date: Optional[date] = None) -> list[Task]:
        """Return all tasks for a given day, sorted by time."""
        if target_date is None:
            target_date = date.today()
        tasks = [t for t in self.owner.get_all_tasks() if t.date == target_date]
        return self.sort_by_time(tasks)

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by their scheduled time (HH:MM string)."""
        return sorted(tasks, key=lambda t: t.time)

    def filter_by_status(self, tasks: list[Task], completed: bool = False) -> list[Task]:
        """Filter tasks by completion status."""
        return [t for t in tasks if t.completed == completed]

    def filter_by_pet(self, tasks: list[Task], pet_name: str) -> list[Task]:
        """Filter tasks belonging to a specific pet."""
        return [t for t in tasks if t.pet_name == pet_name]

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Find tasks scheduled at the same time and return warning strings."""
        warnings = []
        sorted_tasks = self.sort_by_time(tasks)
        for i in range(len(sorted_tasks)):
            for j in range(i + 1, len(sorted_tasks)):
                if sorted_tasks[i].time == sorted_tasks[j].time:
                    a, b = sorted_tasks[i], sorted_tasks[j]
                    warnings.append(
                        f"Conflict: '{a.description}' ({a.pet_name}) and "
                        f"'{b.description}' ({b.pet_name}) are both at {a.time}"
                    )
        return warnings

    def handle_recurring(self, task: Task):
        """If a task is daily or weekly, create the next occurrence on the pet."""
        if task.frequency == "once":
            return
        days = 1 if task.frequency == "daily" else 7
        next_task = Task(
            description=task.description,
            time=task.time,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            frequency=task.frequency,
            pet_name=task.pet_name,
            completed=False,
            date=task.date + timedelta(days=days),
        )
        pet = self.owner.get_pet(task.pet_name)
        if pet:
            pet.add_task(next_task)

    def mark_task_complete(self, task: Task):
        """Mark a task done and schedule the next occurrence if recurring."""
        task.mark_complete()
        self.handle_recurring(task)
