import random

while True:
    user_input = input("Would you like to use the decision maker? ")
    if user_input == "yes":
        cone = input("Enter the first choice: ")
        cto = input("Enter the second choice: ")
        answer = random.choice([cone, cto])
        print("The decision is:", answer)
        
    elif user_input == "no":
        print("Thank you for choosing us. Bye until next time.")
        break
    else: 
        print("Invalid input")
