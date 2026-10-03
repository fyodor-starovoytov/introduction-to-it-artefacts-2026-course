# main.py — the entry point: talks to the user and calls the functions in logic.py
import logic
import matplotlib.pyplot as plt
from PIL import Image

while True:
    userInput = input("Give me a positive integer: ")

    if userInput == "":
        break
    if int(userInput) <= 0:
        print("Invalid input")
        continue

    heartFunction = logic.heart_size(userInput)

    X = logic.mesh_grid(userInput)[0]
    Y = logic.mesh_grid(userInput)[1]

    plt.figure(figsize=(6, 6))
    plt.contour(X, Y, heartFunction, levels=[0], colors='red')
    plt.xlabel("Amount of Love")
    plt.ylabel("Amount of Love")
    plt.title(heartFunction)
    plt.gca().set_aspect('equal')
    plt.grid(True)

    plt.savefig("heart.png")
    print("Graph saved as heart.png")
    img = Image.open("heart.png")
    img.show()

