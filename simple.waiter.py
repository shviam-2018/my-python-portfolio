menu = "black coffe 10nok, latte 10nok, simple coffe 10nok"
great = print("how mey i help you today hear is our menu", menu)
order = input("what do you whant ")

print(great, order)

deal = input("How many " + order + " do you want? ")
print(deal)

price = 10

cal = int(deal) * price
print("your totalle will be", cal)
