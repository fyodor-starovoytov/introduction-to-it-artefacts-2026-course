from leap import is_leap_year

result = is_leap_year(2000)
assert result is True, "got " + str(result)
#A year divisible by 400

result = is_leap_year(2011)
assert result is False, "got " + str(result)
# A year not divisible by 4

result = is_leap_year(2004)
assert result is True, "got " + str(result)
# A year divisible by 4 but not by 100

result = is_leap_year(1900)
assert result is False, "got " + str(result)
# A year divisible by 100 but not by 400

print("All tests passed")
