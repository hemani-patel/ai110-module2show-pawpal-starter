import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session state ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

# --- Header ---
st.title("🐾 PawPal+")
st.caption("A smart pet care planner — add pets, schedule tasks, view your day.")

# --- Add a Pet ---
st.subheader("Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    age = st.number_input("Age", min_value=0, max_value=30, value=3)

if st.button("Add pet"):
    if owner.get_pet(pet_name) is None:
        owner.add_pet(Pet(name=pet_name, species=species, age=age))
        st.success(f"Added {pet_name}!")
    else:
        st.warning(f"{pet_name} already exists.")

if owner.pets:
    st.markdown("**Your pets:** " + ", ".join(
        f"{p.name} ({p.species}, age {p.age})" for p in owner.pets
    ))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Schedule a Task ---
st.subheader("Schedule a Task")

if owner.pets:
    selected_pet = st.selectbox("For which pet?", [p.name for p in owner.pets])
    col1, col2 = st.columns(2)
    with col1:
        task_desc = st.text_input("Task description", value="Morning walk")
        task_time = st.time_input("Scheduled time")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        pet = owner.get_pet(selected_pet)
        pet.add_task(Task(
            description=task_desc,
            time=task_time.strftime("%H:%M"),
            duration_minutes=int(duration),
            priority=priority,
            frequency=frequency,
            pet_name=selected_pet,
        ))
        st.success(f"Added '{task_desc}' for {selected_pet} at {task_time.strftime('%H:%M')}.")
else:
    st.info("Add a pet first, then you can schedule tasks.")

st.divider()

# --- Today's Schedule ---
st.subheader("Today's Schedule")

schedule = scheduler.get_daily_schedule()

if not schedule:
    st.info("No tasks scheduled for today. Add some above!")
else:
    # Conflict warnings
    conflicts = scheduler.detect_conflicts(schedule)
    for c in conflicts:
        st.warning(c)

    if not conflicts:
        st.success("No scheduling conflicts!")

    # Filter controls
    col1, col2 = st.columns(2)
    with col1:
        pet_filter = st.selectbox(
            "Filter by pet",
            ["All pets"] + [p.name for p in owner.pets],
            key="pet_filter",
        )
    with col2:
        status_filter = st.selectbox(
            "Filter by status",
            ["All", "Pending", "Completed"],
            key="status_filter",
        )

    filtered = schedule
    if pet_filter != "All pets":
        filtered = scheduler.filter_by_pet(filtered, pet_filter)
    if status_filter == "Pending":
        filtered = scheduler.filter_by_status(filtered, completed=False)
    elif status_filter == "Completed":
        filtered = scheduler.filter_by_status(filtered, completed=True)

    # Display schedule table
    rows = []
    for t in filtered:
        rows.append({
            "Time": t.time,
            "Task": t.description,
            "Pet": t.pet_name,
            "Duration": f"{t.duration_minutes} min",
            "Priority": t.priority,
            "Frequency": t.frequency,
            "Status": "✅ Done" if t.completed else "⬜ Pending",
        })
    st.table(rows)

    # Mark tasks complete
    st.subheader("Complete a Task")
    pending = scheduler.filter_by_status(schedule, completed=False)
    if pending:
        task_options = [f"{t.time} - {t.description} ({t.pet_name})" for t in pending]
        chosen = st.selectbox("Select a task to mark done", task_options)
        if st.button("Mark complete"):
            idx = task_options.index(chosen)
            scheduler.mark_task_complete(pending[idx])
            st.success(f"Completed! {'Next occurrence scheduled.' if pending[idx].frequency != 'once' else ''}")
            st.rerun()
    else:
        st.success("All tasks for today are done!")
