# checks.py for Lab 5A — copy this over the template's checks.py.
# Three behaviours of count_digits(n). Run with:  python checks.py
import logic

result = logic.count_digits(1234)
assert result == 4, "four digits: got " + str(result)

result = logic.count_digits(7)
assert result == 1, "one digit: got " + str(result)

result = logic.count_digits(0)
assert result == 1, "zero has one digit: got " + str(result)

print("all checks passed")
