import logic

while True:

    a = input("Input Integer a: ")
    b = input("Input Integer b: ")
    c = input("Input Integer c: ")

    if logic.IsNotInteger(a,b,c):
        print("No integer to count")
        break

    tuple = logic.QuadraticSolver(int(a),int(b),int(c))
    print(f"Discriminant is: {tuple[0]}\nx = {f'{tuple[1]:.4f}' if isinstance(tuple[1], (int, float)) else tuple[1]}\nx2 = {tuple[2]}")
        