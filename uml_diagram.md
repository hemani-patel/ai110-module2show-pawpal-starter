# PawPal+ UML Class Diagram

```mermaid
classDiagram
    class Task {
        +str description
        +str time
        +int duration_minutes
        +str priority
        +str frequency
        +bool completed
        +str pet_name
        +date date
        +mark_complete()
    }

    class Pet {
        +str name
        +str species
        +int age
        +list~Task~ tasks
        +add_task(task: Task)
        +remove_task(description: str)
        +get_tasks() list~Task~
    }

    class Owner {
        +str name
        +list~Pet~ pets
        +add_pet(pet: Pet)
        +get_pet(name: str) Pet
        +get_all_tasks() list~Task~
    }

    class Scheduler {
        +Owner owner
        +get_daily_schedule(target_date: date) list~Task~
        +sort_by_time(tasks: list~Task~) list~Task~
        +filter_by_status(tasks: list~Task~, completed: bool) list~Task~
        +filter_by_pet(tasks: list~Task~, pet_name: str) list~Task~
        +detect_conflicts(tasks: list~Task~) list~str~
        +handle_recurring(task: Task)
        +mark_task_complete(task: Task)
    }

    Owner "1" --> "*" Pet : has
    Pet "1" --> "*" Task : has
    Scheduler "1" --> "1" Owner : manages
```
