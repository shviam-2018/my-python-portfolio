import random

import string

# loop to have it run until user whants 
while True:
    
#program start

    user_input = input("do you what to use this password gen?")
    if user_input =="no":
        print ("okay, goodbye")
        break
    elif user_input == "yes":
        pass

# Define the length of the password

    length = int(input("how long should the password be ? "))


# Define the pool of characters to choose from

    characters = string.ascii_letters + string.digits + string.punctuation


# Generate the password

    password = ''.join(random.choice(characters) for i in range(length))


# Print the password

    print(password)