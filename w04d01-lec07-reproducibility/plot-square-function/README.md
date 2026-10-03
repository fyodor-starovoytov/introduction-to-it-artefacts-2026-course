# Y = X² Function Plotter

This program asks the user to enter x values, calculates y = x², and creates a graph.

## Project structure

```text
project/
├── README.md
├── main.py  # takes x values from users and plots the final graph
├── logic.py # calculate_y(x) function located in this file does the main work.
├── checks.py # includes 5 different test cases
├── requirements.txt # lists dependencies of this project
└── .gitignore
```

## Installation

Install the required library:

    python -m pip install -r requirements.txt

## Running the program

Run:

    python main.py

Enter x values separated by spaces.

Example:

-3 -2 -1 0 1 2 3

The graph will be saved as graph.png.

## Checking the program

Run:

    python checks.py