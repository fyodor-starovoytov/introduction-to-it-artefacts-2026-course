import logic

result = logic.QuadraticSolver(1,2,3)
assert result == (-8, "no solution", "no solution"), "got " + str(result)

result = logic.QuadraticSolver(1,2,1)
assert result == (0, -1.000, "no solution"), "got " + str(result)

result = logic.QuadraticSolver(2,5,2)
assert result == (9, -0.5000, -2.0), "got " + str(result)

print("all checks passed")