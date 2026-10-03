from logic import calculate_y


# Test 1: positive numbers
assert calculate_y([1, 2, 3]) == [1, 4, 9]


# Test 2: negative numbers
assert calculate_y([-1, -2, -3]) == [1, 4, 9]


# Test 3: zero
assert calculate_y([0]) == [0]


# Test 4: positive and negative numbers together
assert calculate_y([-2, -1, 0, 1, 2]) == [4, 1, 0, 1, 4]


# Test 5: empty list
assert calculate_y([]) == []


print("All tests passed!")