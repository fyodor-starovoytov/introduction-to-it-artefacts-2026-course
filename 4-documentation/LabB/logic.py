import math
def QuadraticSolver(a, b, c):

    d = b**2 - 4*a*c

    if d<0 or a == 0:
        tup = (d,"no solution", "no solution")
        return tup
    elif d==0:
        x = -b/(2*a)
        tup = (d,x, "no solution")
        return tup
    elif d>0:
        x = (-b+math.sqrt(d))/(2*a)
        y = (-b-math.sqrt(d))/(2*a)
        tup = (d,x,y)
        return tup

def IsNotInteger(a, b, c):
    try:
        intA = int(a)
        intB = int(b)
        intC = int(c)
        return False
    except ValueError:
        return True