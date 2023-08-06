my_dict = {"to-do tasks": []}
while True:
    task = input("What have you planned for the day? ")
    if task.lower() == "quit":
        break
    my_dict["to-do tasks"].append(task)
    print(my_dict)
