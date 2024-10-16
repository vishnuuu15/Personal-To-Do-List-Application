import json
import os

# Task class to represent individual tasks
class Task:
    def __init__(self, title, description, category, completed=False):
        self.title = title
        self.description = description
        self.category = category
        self.completed = completed  # Now accepts completed status

    def mark_completed(self):
        self.completed = True

    def __repr__(self):
        status = 'Completed' if self.completed else 'Not Completed'
        return f"Title: {self.title}, Category: {self.category}, Status: {status}"

# Function to load tasks from tasks.json
def load_tasks():
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as file:
            task_list = json.load(file)
            return [Task(**task) for task in task_list]  # Supports loading completed status
    return []

# Function to save tasks to tasks.json
def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump([task.__dict__ for task in tasks], file, indent=4)

# Function to display all tasks
def view_tasks(tasks):
    if not tasks:
        print("\nNo tasks available.")
        return
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")

# Function to add a new task
def add_task(tasks):
    title = input("\nEnter the task title: ")
    description = input("Enter the task description: ")
    category = input("Enter the task category (e.g., Work, Personal, Urgent): ")
    
    new_task = Task(title, description, category)
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task '{title}' added successfully.")

# Function to mark a task as completed
def complete_task(tasks):
    view_tasks(tasks)
    if tasks:
        task_number = int(input("\nEnter the task number to mark as completed: "))
        if 1 <= task_number <= len(tasks):
            tasks[task_number - 1].mark_completed()
            save_tasks(tasks)
            print("Task marked as completed.")
        else:
            print("Invalid task number.")

# Function to delete a task
def delete_task(tasks):
    view_tasks(tasks)
    if tasks:
        task_number = int(input("\nEnter the task number to delete: "))
        if 1 <= task_number <= len(tasks):
            deleted_task = tasks.pop(task_number - 1)
            save_tasks(tasks)
            print(f"Task '{deleted_task.title}' deleted successfully.")
        else:
            print("Invalid task number.")

# Main menu function
def main():
    tasks = load_tasks()
    
    while True:
        print("\nPersonal To-Do List Application")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            complete_task(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '5':
            save_tasks(tasks)
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == '__main__':
    main()
