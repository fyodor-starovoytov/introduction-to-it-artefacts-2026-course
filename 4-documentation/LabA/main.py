# Lab 5A: move the work into logic.py as a function, keep input()/print() in main.py.
import logic
n = int(input("Give me a whole number: "))
count = logic.count_digits(n)
print("It has", count, "digits.")
