def average(scores):
    total = 0

    for i in range(0, len(scores)):
        total = total + scores[i]

    return total / len(scores)


scores = [2, 4]
print("average:", average(scores))