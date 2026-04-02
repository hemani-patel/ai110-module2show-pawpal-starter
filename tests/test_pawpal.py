from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# --- Basic class tests (from Phase 2) ---

def test_mark_complete():
    task = Task("Walk", "08:00", 30, "high", "daily", "Mochi")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task("Breakfast", "07:00", 10, "high", "daily", "Mochi"))
    assert len(pet.get_tasks()) == 1


# --- Sorting ---

def test_sort_by_time():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)
    owner.add_pet(pet)

    pet.add_task(Task("Evening walk", "18:00", 30, "medium", "daily", "Mochi"))
    pet.add_task(Task("Breakfast", "07:00", 10, "high", "daily", "Mochi"))
    pet.add_task(Task("Lunch", "12:00", 10, "medium", "daily", "Mochi"))

    scheduler = Scheduler(owner)
    schedule = scheduler.get_daily_schedule()
    times = [t.time for t in schedule]
    assert times == ["07:00", "12:00", "18:00"]


# --- Recurrence ---

def test_daily_recurring_creates_next_day():
    today = date.today()
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)
    owner.add_pet(pet)

    task = Task("Breakfast", "07:00", 10, "high", "daily", "Mochi", date=today)
    pet.add_task(task)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(task)

    assert task.completed is True
    assert len(pet.get_tasks()) == 2
    new_task = pet.get_tasks()[1]
    assert new_task.date == today + timedelta(days=1)
    assert new_task.completed is False


def test_weekly_recurring_creates_next_week():
    today = date.today()
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)
    owner.add_pet(pet)

    task = Task("Grooming", "10:00", 60, "low", "weekly", "Mochi", date=today)
    pet.add_task(task)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(task)

    new_task = pet.get_tasks()[1]
    assert new_task.date == today + timedelta(days=7)


def test_once_task_does_not_recur():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)
    owner.add_pet(pet)

    task = Task("Vet visit", "14:00", 60, "high", "once", "Mochi")
    pet.add_task(task)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(task)

    assert len(pet.get_tasks()) == 1  # no new task created


# --- Conflict detection ---

def test_detect_conflicts_same_time():
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog", 3)
    whiskers = Pet("Whiskers", "cat", 5)
    owner.add_pet(mochi)
    owner.add_pet(whiskers)

    mochi.add_task(Task("Vet", "10:00", 60, "high", "once", "Mochi"))
    whiskers.add_task(Task("Play", "10:00", 20, "medium", "daily", "Whiskers"))

    scheduler = Scheduler(owner)
    schedule = scheduler.get_daily_schedule()
    conflicts = scheduler.detect_conflicts(schedule)
    assert len(conflicts) == 1
    assert "10:00" in conflicts[0]


def test_no_conflicts_different_times():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog", 3)
    owner.add_pet(pet)

    pet.add_task(Task("Walk", "08:00", 30, "high", "daily", "Mochi"))
    pet.add_task(Task("Feed", "12:00", 10, "high", "daily", "Mochi"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts(scheduler.get_daily_schedule())
    assert conflicts == []


# --- Edge cases ---

def test_pet_with_no_tasks():
    owner = Owner("Jordan")
    owner.add_pet(Pet("Mochi", "dog", 3))

    scheduler = Scheduler(owner)
    schedule = scheduler.get_daily_schedule()
    assert schedule == []
    assert scheduler.detect_conflicts(schedule) == []


def test_owner_get_pet_not_found():
    owner = Owner("Jordan")
    assert owner.get_pet("Ghost") is None
