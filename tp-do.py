import random

# Create a list to store the tasks
tasks = []

# Function to add a task to the list
def add_task(task):
  tasks.append(task)

# Function to remove a task from the list
def remove_task(task):
  tasks.remove(task)

# Function to mark a task as done
def mark_task_done(task):
  task["done"] = True

# Function to generate a random task
def generate_random_task():
  return {"task": random.choice(["Do the dishes", "Take out the trash", "Clean your room", "Go for a walk", "Study for your test"]), "done": False}

# Function to display the to-do list
def display_to_do_list():
  print("To-do list:")
  for task in tasks:
    print(f"* {task['task']}")

# Main loop
while True:
  # Display the to-do list
  display_to_do_list()

  # Get the user's input
  user_input = input("What do you want to do? (add, remove, mark done, generate, cancel): ")

  # Process the user's input
  if user_input == "add":
    task = input("Enter a task: ")
    add_task(task)
  elif user_input == "remove":
    task = input("Enter a task to remove: ")
    remove_task(task)
  elif user_input == "mark done":
    task = input("Enter a task to mark as done: ")
    mark_task_done(task)
  elif user_input == "generate":
    task = generate_random_task()
    add_task(task)
  elif user_input == "cancel":
    break

