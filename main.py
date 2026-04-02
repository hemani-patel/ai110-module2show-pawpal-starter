from pawpal_system import Task, Pet, Owner, Scheduler

owner = Owner("Jordan")

mochi = Pet(name="Mochi", species="dog", age=3)
whiskers = Pet(name="Whiskers", species="cat", age=5)
owner.add_pet(mochi)
owner.add_pet(whiskers)

# Add tasks out of order to show sorting works
mochi.add_task(Task("Morning walk", "08:00", 30, "high", "daily", "Mochi"))
mochi.add_task(Task("Breakfast", "07:00", 10, "high", "daily", "Mochi"))
mochi.add_task(Task("Vet appointment", "10:00", 60, "high", "once", "Mochi"))
whiskers.add_task(Task("Feed Whiskers", "07:30", 10, "high", "daily", "Whiskers"))
whiskers.add_task(Task("Play time", "10:00", 20, "medium", "daily", "Whiskers"))

scheduler = Scheduler(owner)

# 1. Sorted daily schedule
print("=== Today's Schedule (sorted by time) ===\n")
schedule = scheduler.get_daily_schedule()
for t in schedule:
    print(f"  {t.time}  {t.description:<20} ({t.pet_name})  [{t.priority}]")

# 2. Conflict detection — Mochi vet and Whiskers play are both at 10:00
print("\n=== Conflict Check ===\n")
conflicts = scheduler.detect_conflicts(schedule)
if conflicts:
    for c in conflicts:
        print(f"  ! {c}")
else:
    print("  No conflicts.")

# 3. Filter by pet
print("\n=== Mochi's Tasks Only ===\n")
mochi_tasks = scheduler.filter_by_pet(schedule, "Mochi")
for t in mochi_tasks:
    print(f"  {t.time}  {t.description}")

# 4. Recurring: complete a daily task and see next occurrence created
print("\n=== Recurring Task Demo ===\n")
breakfast = mochi.get_tasks()[1]  # Breakfast
print(f"  Completing '{breakfast.description}' for {breakfast.date}...")
scheduler.mark_task_complete(breakfast)
print(f"  Completed: {breakfast.completed}")

all_breakfasts = [t for t in mochi.get_tasks() if t.description == "Breakfast"]
for t in all_breakfasts:
    status = "Done" if t.completed else "Pending"
    print(f"  -> {t.description} on {t.date} [{status}]")

# 5. Filter by status
print("\n=== Pending Tasks Only ===\n")
pending = scheduler.filter_by_status(schedule, completed=False)
for t in pending:
    print(f"  {t.time}  {t.description:<20} ({t.pet_name})")
