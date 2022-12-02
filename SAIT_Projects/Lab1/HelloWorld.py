name = input("What is your name? ")
birth_year = int(input("What is your birth year? "))
print(f"Hello, {name}!")


from datetime import datetime

this_year = datetime.now().year


age =  this_year - birth_year
print(f"You must be {age} years old.")

print("Goodbye...")


