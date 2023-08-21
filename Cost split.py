while True:

    TA = input("how much do you what to split: ")

    SA = input("split among how many people? ")


    cal = float(TA) / float(SA)

    print("you'r per head is:",cal)
    
    Again = input("do you what to use it again? ")
    if Again == "yes":
        pass
    elif Again == "no":
        break
    else: print("not a valid answer.")