while True:
    start_command = input("Would you like to use my math table calculator (Y/N): ").strip()

    if start_command == "y":
      n = int(input("What mathematical table do you need: ").strip())

      for i in range(1, 11):
        result = n * i
        print(f"{n} x {i} = {result}")

    elif start_command == "n":
      print("Thanks for using me!")
      break
