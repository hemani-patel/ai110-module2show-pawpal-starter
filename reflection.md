# PawPal+ Project Reflection

## 1. System Design

**Core user actions:**

1. **Add and manage pets** — A user can register pets with basic info (name, species, age) and manage their roster of furry companions.
2. **Schedule care tasks** — A user can create tasks for each pet (walks, feedings, medications, appointments) with a specific time, duration, priority, and frequency (one-time, daily, weekly).
3. **View today's organized schedule** — A user can generate a sorted daily plan across all pets, see conflict warnings when tasks overlap, and track task completion.

**a. Initial design**

The system uses four classes:

- **Task** (dataclass): Represents a single care activity. Holds description, scheduled time, duration, priority, frequency, completion status, associated pet name, and date. Responsible for marking itself complete.
- **Pet** (dataclass): Stores pet details (name, species, age) and maintains a list of tasks. Responsible for adding/removing its own tasks.
- **Owner**: Manages the user's profile and a collection of pets. Provides access to all tasks across every pet.
- **Scheduler**: The scheduling "brain." Takes an Owner and orchestrates the daily plan — sorting tasks by time, filtering by pet or status, detecting time conflicts, and handling recurring task generation.

**b. Design changes**

- Added `mark_task_complete()` to the Scheduler class in Phase 4. The original skeleton only had `handle_recurring()`, but it made more sense to have a single method that marks a task done *and* handles recurrence in one call. This keeps the calling code (in `app.py` and `main.py`) simple — one method instead of two.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler sorts tasks by **time** (HH:MM), which is the primary constraint — a pet owner needs to know what to do first.
- It also filters by **completion status** (pending vs. done) and by **pet name**, so the owner can focus on what's left or on a specific pet.
- Time was the most important constraint because a daily care routine is fundamentally about "what happens when."

**b. Tradeoffs**

- Conflict detection only checks for **exact time matches**, not overlapping durations. Two tasks at 10:00 trigger a warning, but a 30-minute task at 9:45 and a task at 10:00 do not.
- This is reasonable because it keeps the logic simple and still catches the most common scheduling mistake (double-booking a time slot). A duration-aware overlap check would add complexity without much benefit for a typical pet care schedule.

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI (Cursor agent mode) for every phase: brainstorming the class design and UML, scaffolding class skeletons, implementing method logic, generating tests, and wiring the Streamlit UI.
- The most helpful prompts were specific and scoped — e.g., "create class skeletons based on this UML" or "implement sorting by HH:MM time." Broad prompts like "make my app better" were less useful than targeted ones.

**b. Judgment and verification**

- The AI initially included a `timedelta` import in the Phase 1 skeleton even though recurring tasks weren't implemented yet. I removed it to keep the skeleton minimal and only added it back in Phase 4 when the code actually needed it.
- I verified AI output by running `main.py` after every change and checking that the terminal output matched expectations, plus running `pytest` to confirm nothing broke.

---

## 4. Testing and Verification

**a. What you tested**

- Task completion (mark_complete flips the status), adding tasks to a pet, sorting by time, daily and weekly recurrence, one-time tasks not recurring, conflict detection for same-time tasks, no false positives for different times, empty pet schedule, and looking up a missing pet.
- These tests are important because they cover both the "happy path" (normal usage) and edge cases (empty data, missing lookups). Sorting and recurrence are the core algorithmic behaviors — if they break, the whole scheduler is wrong.

**b. Confidence**

- 4 out of 5 stars. Every feature has at least one test, and all 10 pass.
- With more time I would test: overlapping durations (not just exact time matches), completing a recurring task multiple times in a row, and tasks that span midnight.

---

## 5. Reflection

**a. What went well**

- The "CLI-first" workflow. Building and verifying everything in `main.py` before touching the Streamlit UI meant the backend was solid by the time I wired it up. The UI integration was smooth because the logic was already tested.

**b. What you would improve**

- I would add duration-aware conflict detection (checking for overlapping time ranges, not just exact matches). I'd also add the ability to edit or reschedule existing tasks from the UI rather than only adding new ones.

**c. Key takeaway**

- Designing the structure first (UML and skeletons) before writing any logic made the whole project easier. When I acted as the "lead architect" and kept the design simple, the AI was most effective at filling in the implementation details. The clearer my design intent, the better the AI output.
