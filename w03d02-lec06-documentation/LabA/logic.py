def count_digits(n):
    count = 0
    if n == 0:
        return count + 1
    while n > 0:
        n = n // 10
        count = count + 1
    return count