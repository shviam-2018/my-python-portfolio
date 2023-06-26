email = input("Enter email: ").strip()

username, domain = email.split('@')

print(f"Your username is {username} and domain is {domain}")
