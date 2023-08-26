#add's a infinity loop
while True:
    
    #this ask the user if they what to use my cod or not 
    user_input = input("would you like to use leap year checker? (yes or no): ")

    #if the user replays yes the code exucutes 
    if user_input == "yes":

        def is_leap(year):
            leap = False

        #this is all the cal that is needed to find leap year
            # Write your logic here
            leap = year % 4 == 0 and year % 100 != 0 or year % 400 == 0

            return leap

        #this one asked what year are you wondering is a leap year
        year = int(input("what year do you what to check: "))

        #this one tells you is it is a leap year or not
        print(is_leap(year),"thanks for uesing")

    #and if the user say no thay dont what to use this code it braks the loop/ ends the code
    elif user_input == "no":
        print("hope to see you soon")
        break
    
    #this mesg is if you try to enter something else then yes or no i.e. lolno or yass!
    else:
        print("Please enter 'yes' or 'no'.")
