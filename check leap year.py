def is_leap(year):
    leap = False

    # Write your logic here
    leap = year % 4 == 0 and year % 100 != 0 or year % 400 == 0

    return leap

year = int(input("what year do you what to check: "))

print(is_leap(year))
