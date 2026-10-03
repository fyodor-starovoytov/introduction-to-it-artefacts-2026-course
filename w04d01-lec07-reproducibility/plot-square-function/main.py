import matplotlib.pyplot as plt

from logic import calculate_y

x = input("Enter x values, separated by spaces: ")
x = [int(number) for number in x.split()]

y = calculate_y(x)

plt.plot(x, y, "o-")
plt.xlabel("x")
plt.ylabel("y")
plt.title("y = x²")

plt.savefig("graph.png")
print("Graph saved as graph.png")