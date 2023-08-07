import time

my_dict = {"to-do tasks": []}

while True:
    task = input("What have you planned for the day? ")
    if task.lower() == "quit":
        break
    my_dict["to-do tasks"].append(task)
    print(my_dict)

# Get the current time in 24-hour format
current_time = time.strftime("%H:%M")

if current_time == "00:00":
    # Clear the to-do tasks list if the time is 00:00 (midnight)
    my_dict["to-do tasks"] = []

print("Your to-do list for the day:")
print(my_dict["to-do tasks"])
