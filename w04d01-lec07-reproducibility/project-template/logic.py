import numpy as np
import math
def heart_size(z :int):
    """Returns a function that draws a heart with given z parameter."""
    """z stands for size of the heart"""
    x = mesh_grid(z)[0]
    y = mesh_grid(z)[1]

    function = (x**2 + y**2 - int(z))**3 - x**2 * y**3

    return function

def mesh_grid(z):
    """Gets the grid size"""
    x = np.linspace(-(int(z)/3+2), int(z)/3+2, 400)
    y = np.linspace(-(int(z)/3+2), int(z)/3+2, 400)
    X,Y = np.meshgrid(x, y)

    return X, Y