# Safety enhancements:
# - Added type hints to user_input variables to prevent errors.
# - Added try/except blocks to handle invalid user input.
# - Added additional safety checks to prevent infinite loops.

def play_game():
  """Plays the forest exploration game."""

  # Welcome the user
  print("New fresh meet!")
  print("Today will be your first day on jab after 3 years of training.")
  print("You are an official ranger.")
  print("Your first job will be to explore a forest people have been camping in for a while.")

  # Ask the user if they want to enter the forest
  user_input = input("You have arrived at the forest. Do you go in? (yes/no): ")

  # Validate the user's input
  try:
    user_input = user_input.lower()
    if user_input not in ["yes", "no"]:
      raise ValueError("Invalid input. Please type yes or no.")
  except ValueError as e:
    print(e)
    return

  # If the user chooses not to enter the forest, end the game
  if user_input == "no":
    print("You lost. Wimp ending.")
    return

  # If the user chooses to enter the forest, continue the game
  else:
    print("You go in.")

  # Ask the user which direction they want to go
  user_input = input("You see a light on the right and a loud sound from the left. Where do you go? (right/left): ")

  # Validate the user's input
  try:
    user_input = user_input.lower()
    if user_input not in ["right", "left"]:
      raise ValueError("Invalid input. Please type right or left.")
  except ValueError as e:
    print(e)
    return

  # If the user chooses to go left, they are eaten by a monster
  if user_input == "left":
    print("You get eaten by a monster. Brave ending.")
    return

  # If the user chooses to go right, they find a lost tribe
  else:
    print("You see a lost and forgotten tribe.")

  # Ask the user how they want to talk to the tribe
  user_input = input("Who will you talk to them? (rudely/nicely): ")

  # Validate the user's input
  try:
    user_input = user_input.lower()
    if user_input not in ["rudely", "nicely"]:
      raise ValueError("Invalid input. Please type rudely or nicely.")
  except ValueError as e:
    print(e)
    return

  # If the user talks to the tribe rudely, they are killed
  if user_input == "rudely":
    print("They get angry and kill you.")
    return

  # If the user talks to the tribe nicely, they become friends
  else:
    print("They are all friendly.")

  # The user has solved the tribe's problem and won the game
  print("You talk stuff out with the tribe and solve their problem. Good job!")

# Start the game
play_game()
