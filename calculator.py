import math
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

def sqrt(num):
    if num < 0:
        return False
    num = math.sqrt(num)
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
        return None
    answer = float(nums[0])
    if str(answer).endswith(".0"):
        return int(answer)
    return answer


def simplify(expression,o):

    global ans

    if "clr" in expression:
        return None

    elif o =='c':
        return functions(expression)
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

            y += [functions(expression)]

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

            Un += [functions(expression)]
            print(Un[i])

        n = [int(n)]+ [i for i in range(int(n)+1,Ux)]
        print(n)
        print(Un)
        """plt.scatter(n, Un)
        plt.grid()
        plt.show()"""

        return Un[-1]


    else:

        return functions(expression)
def functions(expression):

    global ans
    func = True
    while func == True:

        if "ans" in expression:
            ans = str(ans)
            f = expression.find("ans")
            expression = expression.replace("ans", ans)

        elif "rand(" in expression:
            f = expression.find("rand(")
            l = expression.find(")", f)
            split = expression.find(",", f, l)
            floor = expression[f + 5:split]
            roof = expression[split + 1:l]

            num = random(floor,roof)
            expression = expression[:f] + num + expression[l + 1:]

        elif "|" in expression:

            f = expression.find("|") + 1
            l = expression.find("|", f)
            num = expression[f:l]

            expression = expression[:f - 1] + abv(mathy(num)) + expression[l + 1:]

        elif "sqrt" in expression:
            f = expression.find("sqrt(") + 5
            l = expression.find(")", f)
            num = expression[f:l]


            expression = expression[:f - 5] + sqrt(mathy(num)) + expression[l + 1:]

        elif "sin(" in expression:
            f = expression.find("sin(")
            l = expression.find(")", f)
            num = expression[f+4:l]

            num = str(math.sin(float(num)))

            expression = expression[:f] +  str(math.tan(mathy(num))) + expression[l + 1:]
        elif "cos(" in expression:
            f = expression.find("cos(")
            l = expression.find(")", f)
            num = expression[f + 4:l]
            print(num)
            expression = expression[:f] + str(math.cos(mathy(num))) + expression[l + 1:]
        elif "tan(" in expression:
            f = expression.find("tan(")
            l = expression.find(")", f)
            num = expression[f + 4:l]

            expression = expression[:f] + str(math.tan(mathy(num))) + expression[l + 1:]

        else:
            func = False
    if func == False:

        return sort(expression)

def fx(expression):
    
    z = np.arange(-15,15,0.25)
    x = [z[i] for i in range(len(z))]
    y = []

    print(expression, "1st")
    for j in range(len(expression)):
        if expression[j] == "x":
            if expression[j - 1].isnumeric() == True or expression[j-1] == ')':
                expression = expression[:j] + "*x" + expression[j + 1:]
    print(x)
    xpression = expression
    for i in range(len(x)):


        expression = xpression.replace("x", str(x[i]))

        expression = expression.replace("--", "+")
        expression = expression.replace("-+", "-")
        expression = expression.replace("++", "+")
        expression = expression.replace("+-", "-")

        y += [functions(expression)]

    plt.scatter(x, y)

    plt.grid()
    plt.show()
    plt.savefig('/static/plt.png')  # save the figure to file
    plt.close(plt)
    




def mathy(x):

    return functions(x)




