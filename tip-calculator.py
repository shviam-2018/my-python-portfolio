#this is a tip calculater made for my python portfolio

#this creats input that ask how much is the bill and then comfierms it with a while true loop that brakes when the user say "yes".
while True:
    TB = int(input("what is the total Bill: "))
    print("Your bill without tip:",TB)
    confirmTB = input("is this coreect: ")
    if confirmTB == "no":
        pass
    elif confirmTB =="yes":
        break
    
#this is the same as the last one the differenfs is that this one comfiers that the Tip enterd is coreact.    
while True:
    TT = float(input("what is the tip percentage: "))
    print("Your tip percentage:",TT)
    confirmTT = input("is this coreect: ")
    if confirmTT == "no":
        pass
    elif confirmTT =="yes":
        break
    
#this calculates the total bill with tip included.    
BAT = TB + (TT/100)

#this prints the bill with tip included
print("Your bill with tip:",BAT)
