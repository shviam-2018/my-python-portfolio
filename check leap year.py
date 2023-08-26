def is_leap(year):
    leap = False

    # Write your logic here
    if year % 4 == 0:
        leap = True
    elif year % 100 == 0:
        leap = False
    elif year % 400 == 0:
        leap = True
    else:
        leap = False

    return leap

year = int(input("what year do you what to check: "))
 
print(is_leap(year))