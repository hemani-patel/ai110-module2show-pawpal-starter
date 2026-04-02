# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

i focused on 3 mian things which a user should be able to do which are add pets, schedule tasks for them, and see a schedule. I descigned the sistem using 4 mian classes. Task is a single activity like feeding or walking, storing things like time, duration, etc and if it's completed. It also has method to mark task as complete. Pet stores info about each pet and tracks all of its tasks, it also adds and manages those tasks. Owner manages multiple pets and gives access to get all tasks across pets. Scheduler is the logic layer, taking all the tasks form the owneer and organizes them into daily schedule, sorted by time, detcts conflits, and handles recurrnig tasks. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes my design changed during implementation. I added a mark_task_complete() method inside Schedueler. At first i had a seperate method for handling just recurring tasks but it felt easier to combine marking a task complete and creating the next recurring tasks in 1 step. I think this change made the flow simpler and cleaner. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The main constraint which I focused on was time. The scjeduler sorts tasks by time as thats what matters most for dailt routines. I also considered if a task was compelete or not and filtering tasks by pet. Time was the highest priority, although, since the whole purpose of the app is to organize a daily schedule. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

one tradeoff I made was conflict detection. right now the system only detects conflicts if 2 tasks have the same start time. It doesnt check overlapping times. I think this is a reasonable tradeoff becayse it keeps the logic simpler and still is able to catch some conflicts. Adding full overlap detction would be very complex. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Ai throughout the whole project to help me design teh system, create skeletons for the class,writing tests, and debugging. The most helpful prompts were specfic prompts. For example, asking how to implement sorting by time or how different classes should interact. When i aksed more general questions, the asnwers weren't as useful.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

There was a point where AI added a timedelta import even though i wasnt using recurrence yet. I removed it because i wanted to keep the code clean and only include necessary things. Later, when i implemented recurring tasts I had to add it back. To amke sure that everthing worked I tested my code constabtly running main.py to check output and using pyttest to make sure my test cases were being passed as well. These steps helped me check the AI code. 
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested many key behvaiores. For example, adding takss to a pet, detetcing conflucts at the same time, handling cases with no tasks, making sure one time tasks dont get repeated and etc. These tests were very important becayse they cover normal and edge case usage. This was espcially important for sorting and recurrence since those are the main parts of the logic for the scheduler. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I think I am pretty confident that my scheduler works correctly. all of my test cases passed and the main fucntionality functions as i would expect it to . If i had more time I would test overlapping task durations (not just exact time macthes). completing recurrinhg tasks multiple times in a row, and edge cases like if tasks go past midnight. 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The CLI- afirst approach worked really well and I am most satified with that. Building and testing everything in main.py first made sure my backend logic was good before I thought about the UI at all. Then when i moved on to think about the UI everything went more smoothly.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If i had more time I would  add features to edit or reschedule tasks. Right now the system mostly focuses on adding and completing tasks. Also i would improve the conflciut detection logic.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

My key takeaway from this project is how important it is to design. the system first before coding. Once I had a clear structure everyhing was easier. Also, AI is way more helpful when given very specific instructions on what I want or need to be fixed. 