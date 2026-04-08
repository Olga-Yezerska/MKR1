import os
from datetime import datetime

FILE = 'tasks.txt'

def load():
    tasks = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                    parts = line.strip().split("|")
                    if len(parts) == 5:
                        task_id = int(parts[0])
                        desc = parts[1]
                        date = parts[2]
                        priority = int(parts[3])
                        done = parts[4] == "True"
                        tasks.append({
                            "id": task_id,
                            "description": desc,
                            "date": date,
                            "priority": priority,
                            "done": done
                        })
    return tasks

def save_tasks(tasks):
     with open(FILE, "w", encoding="utf-8") as f:
          for task in tasks:
               f.write(f"{task['id']}|{task['description']}|{task['date']}|"f"{task['priority']}|{task['done']}\n")

def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

def add_task(description: str, priority: int, date=None):
    if not (1 <= priority <= 5):
        raise ValueError("Invalid priority")
    if not description or not description.strip():
        raise ValueError("Invalid description")
    
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
        
    tasks = load()
    task_id = get_next_id(tasks)

    tasks.append({
        "id": task_id,
        "description": description,
        "date": date,
        "priority": priority,
        "done": False
    })

    save_tasks(tasks)
    return task_id

