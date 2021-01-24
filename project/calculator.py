from math import *
import random as rand
import matplotlib.pyplot as plt
import time
import numpy as np







def random(floor, celing):
    return str(rand.randint(int(floor), int(celing)))

def abv(num):
    if num < 0:
        num = num - (2 * num)
    return str(num)



def pfctSqr(num):
    num = sqrt(num)
    num = str(num)
    x = num.split(".")
    if x[1] != "0":
        return False
    return True

def divsi(num, div):
    if num % div == 0:
        return True
    return False

def prime(num):
    x = 0
    for i in range(1, num + 1):
        if num % i == 0:
            x += 1
    if x > 2:
        return False
    return True

def calculate():
    global Dbz
    if len(nums) == 1 and len(operations) == 1:

        x = float(nums.pop(0))
        oper = operations.pop(0)
        if oper == "-":
            nums.insert(0, -x)
        else:
            nums.insert(0, x)
        return

    x = float(nums.pop(0))
    y = float(nums.pop(0))
    oper = operations.pop(0)
    if oper == "*":
        nums.insert(0, (y * x))
    elif oper == "/":
        try:
            nums.insert(0, (y / x))
        except:
            Dbz = True
    elif oper == "+":
        nums.insert(0, (y + x))
    elif oper == "-":
        nums.insert(0, (y - x))
    elif oper == "^":
        nums.insert(0, y ** x)

def sort(inpt):
    global Dbz
    Dbz = False
    global nums
    global operations
    nums = []
    operations = []
    neg = False

    for i in range(len(inpt)):

        char = inpt[i]
        if Dbz == True:
            print('portal1')
            return None
        if neg == True:
            a = nums.insert(0, int(str("-" + char)))
            neg = False
        elif i != 0 and char == "-" and inpt[i-1].isnumeric() == False:
            neg = True
        elif char == "+" or char == "-":
            while (not len(operations) == 0) and (operations[0] != "("):
                calculate()
            operations.insert(0, char)
        elif char == "*" or char == "/":

            while (not len(operations) == 0) and (operations[0] == "*" or operations[0] == "/"):
                calculate()
            operations.insert(0, char)
        elif char == "^":

            operations.insert(0, char)
        elif char == "(":
            operations.insert(0, char)
        elif char == ")":
            while operations[0] != "(":
                calculate()
            operations.pop(0)

        else:

            if i == 0:
                a = nums.insert(0, int(char))
            elif inpt[i - 1].isnumeric() or inpt[i - 1] == ".":

                nums[0] = str(nums[0]) + char
            else:
                a = nums.insert(0, int(char))
    while not len(operations) == 0:

        calculate()


    if Dbz == True:
        print("division by zero :/")
        print('portal2')
        return None
    try:
        answer = float(nums[0])
    except:
        print('portal')
        return None
    else:
        if str(answer).endswith(".0"):
            return int(answer)
        return answer


def simplify(expression,o):

    global ans

    if "clr" in expression:
        return None

    elif o =='c':
        return 3#functions(expression)
    elif expression[0:2] == "y=":
        l = int(input("interval: "))
        expression = expression[2:]
        z = np.arange(-l,l,0.25)
        x = [z[i] for i in range(len(z))]
        y = []

        print(expression, "1st")
        for j in range(len(expression)):
            if expression[j] == "x":
                if expression[j - 1].isnumeric() == True:
                    expression = expression[:j] + "*x" + expression[j + 1:]

        xpression = expression
        print(expression, "new expression")
        for i in range(len(x)):


            expression = xpression.replace("x", str(x[i]))

            expression = expression.replace("--", "+")
            expression = expression.replace("-+", "-")
            expression = expression.replace("++", "+")
            expression = expression.replace("+-", "-")

            #y += [functions(expression)]

        plt.scatter(x, y)

        plt.grid()
        plt.show()
        print("u")
        return
    elif expression[0] == "U" and expression[2] == "="  and expression[1].isnumeric():

        Un = [int(expression[3:])]
        n = str(expression[1])

        expression = input("Un+1=")
        Ux = int(input("Calculate U"))+1

        for j in range(len(expression)-1):
            if expression[j:j+1] == "Un":
                if expression[j - 1].isnumeric() == True:
                    expression = expression[:j] + "*Un" + expression[j + 1:]

        xpression = expression
        print(expression)
        for i in range(Ux - int(n)+1):
            expression = xpression.replace("Un", str(Un[i-1]))
            expression = expression.replace("--", "+")
            expression = expression.replace("-+", "-")
            expression = expression.replace("++", "+")
            expression = expression.replace("+-", "-")

            #Un += [functions(expression)]
            print(Un[i])

        n = [int(n)]+ [i for i in range(int(n)+1,Ux)]
        print(n)
        print(Un)
        """plt.scatter(n, Un)
        plt.grid()
        plt.show()"""

        return Un[-1]


    else:

        return 3#functions(expression)


def fx(expression,ranges):
    
    z = np.arange(0-ranges, float(ranges + 0.25), 0.25)

    x = [i for i in z]
    y = []




    for j in range(len(expression)):

        if expression[j] == "x":
            if expression[j - 1].isnumeric() == True or expression[j-1] == ')':
                expression = expression[:j] + "*x" + expression[j + 1:]

    for i in x:
        f = {"x": i, 'cos': cos, 'tan':tan, 'sin':sin,'sqrt':sqrt,'pi':pi,"e":e,'abs':fabs,"π":pi}


        try:
            y += [eval(expression, f)]
        except:
            y += [None]

    return x, y



