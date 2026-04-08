import os
from datetime import datetime

FILE = 'tasks.txt'

def load():
    tasks = []
    if not os.path.exists(FILE):
        return tasks
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                parts = line.strip().split("|")
                if len(parts) == 5:
                    try:
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
                    except ValueError:
                        continue
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

def delete_task(task_id: int):
     tasks = load()
     if not tasks:
          raise ValueError("Tasks list is empty")
     
     for i, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[i]
            save_tasks(tasks)
            return
     raise ValueError(f"Task not found")

def view_tasks():
     tasks = load()
     if not tasks:
          print("Tasks list is empty.")
          return
     
     print("\n=== Tasks List ===")
     print("1. Sort by priority")
     print("2. Sort by date")
     choice = input("Select option for sort: ").strip()
    
     if choice == "1":
         tasks.sort(key=lambda x: (x["priority"], x["date"]))
     else:
         tasks.sort(key=lambda x: (x["date"], x["priority"]))
    
     for task in tasks:
         status = "Done" if task["done"] else "Not completed"
         print(f"[{status}] ID: {task['id']:2d} | Priority: {task['priority']} | "f"Date: {task['date']} | {task['description']}")
     

def mark_task(task_id: int):
     tasks = load()
     if not tasks:
          raise ValueError("Tasks list is empty")
     
     for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                print(f"Task {task_id} is already marked as done.")
            else:
                task["done"] = True
                save_tasks(tasks)
            return
     raise ValueError(f"Task not found")

def main():
    if not os.path.exists(FILE):
        open(FILE, 'w', encoding='utf-8').close()

    while True:
        print("\n" + "=" * 55)
        print("          TASK MANAGEMENT")
        print("=" * 55)
        print("1. Add new task")
        print("2. Delete task")
        print("3. View all tasks")
        print("4. Mark task as completed")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        try:
            if choice == "1":
                desc = input("Enter task description: ").strip()
                prio = int(input("Enter priority (1-5): "))
                date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
                date = date_str if date_str else None
                task_id = add_task(desc, prio, date)
                print(f"Task ID = {task_id}")

            elif choice == "2":
                tid = int(input("Enter task ID to delete: "))
                delete_task(tid)
                print(f"Task {tid} deleted.")

            elif choice == "3":
                view_tasks()

            elif choice == "4":
                tid = int(input("Enter task ID to mark as done: "))
                mark_task(tid)

            elif choice == "5":
                print("Program ends")
                break
            else:
                print("Invalid choice")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()