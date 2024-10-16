import json
import os
import tkinter as tk
from tkinter import messagebox

# Task class to represent individual tasks
class Task:
    def __init__(self, title, description, category, completed=False):
        self.title = title
        self.description = description
        self.category = category
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def __repr__(self):
        return f"{self.title} ({self.category}) - {'Completed' if self.completed else 'Not Completed'}"

# Function to load tasks from tasks.json
def load_tasks():
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as file:
            task_list = json.load(file)
            return [Task(**task) for task in task_list]
    return []

# Function to save tasks to tasks.json
def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump([task.__dict__ for task in tasks], file, indent=4)

# GUI Class for the To-Do List Application
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal To-Do List Application")
        
        self.tasks = load_tasks()

        # Task List Frame
        self.task_list_frame = tk.Frame(root)
        self.task_list_frame.pack(pady=10)

        # Listbox to display tasks
        self.task_listbox = tk.Listbox(self.task_list_frame, height=10, width=50)
        self.task_listbox.pack(side=tk.LEFT)

        # Scrollbar for task listbox
        self.scrollbar = tk.Scrollbar(self.task_list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        # Buttons
        self.add_button = tk.Button(root, text="Add Task", width=15, command=self.add_task)
        self.add_button.pack(pady=5)

        self.complete_button = tk.Button(root, text="Mark as Completed", width=15, command=self.complete_task)
        self.complete_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Task", width=15, command=self.delete_task)
        self.delete_button.pack(pady=5)

        # Load tasks into the listbox
        self.refresh_task_list()

    # Function to add a new task
    def add_task(self):
        task_window = tk.Toplevel(self.root)
        task_window.title("Add New Task")

        tk.Label(task_window, text="Title").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(task_window, text="Description").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(task_window, text="Category").grid(row=2, column=0, padx=10, pady=10)

        title_entry = tk.Entry(task_window, width=40)
        title_entry.grid(row=0, column=1, padx=10, pady=10)

        description_entry = tk.Entry(task_window, width=40)
        description_entry.grid(row=1, column=1, padx=10, pady=10)

        category_entry = tk.Entry(task_window, width=40)
        category_entry.grid(row=2, column=1, padx=10, pady=10)

        def save_new_task():
            title = title_entry.get()
            description = description_entry.get()
            category = category_entry.get()

            if title and category:
                new_task = Task(title, description, category)
                self.tasks.append(new_task)
                save_tasks(self.tasks)
                self.refresh_task_list()
                task_window.destroy()
            else:
                messagebox.showwarning("Input Error", "Title and Category are required!")

        save_button = tk.Button(task_window, text="Save Task", command=save_new_task)
        save_button.grid(row=3, column=1, pady=10)

    # Function to mark a task as completed
    def complete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks[selected_task_index[0]]
            task.mark_completed()
            save_tasks(self.tasks)
            self.refresh_task_list()
            messagebox.showinfo("Task Completed", f"Task '{task.title}' marked as completed.")
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

    # Function to delete a task
    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks.pop(selected_task_index[0])
            save_tasks(self.tasks)
            self.refresh_task_list()
            messagebox.showinfo("Task Deleted", f"Task '{task.title}' deleted successfully.")
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    # Function to refresh the task list in the listbox
    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

# Main function to run the GUI application
if __name__ == '__main__':
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
