import math
import random as rand

b = 5
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
        nums.insert(0, (y / x))
    elif oper == "+":
        nums.insert(0, (y + x))
    elif oper == "-":
        nums.insert(0, (y - x))
    elif oper == "^":
        nums.insert(0, y ** x)


def sort(inpt):
    global nums
    global operations
    nums = []
    operations = []

    for i in range(len(inpt)):

        char = inpt[i]

        if char == "+" or char == "-":
            while (not len(operations) == 0) and (operations[0] != "("):
                calculate()
            operations.insert(0, char)
        elif char == "*" or char == "/" or char == "^":
            while (not len(operations) == 0) and (operations[0] == "*" or operations[0] == "/" or operations[0] == "^"):
                calculate()
            operations.insert(0, char)
        elif char == "(":
            operations.insert(0, char)
        elif char == ")":
            while operations[0] != "(":
                calculate()
            operations.pop()
        else:
            if i == 0:
                a = nums.insert(0, int(char))
            elif inpt[i - 1].isnumeric() or inpt[i - 1] == ".":

                nums[0] = str(nums[0]) + char
            else:
                a = nums.insert(0, int(char))

    while not len(operations) == 0:
        calculate()

    answer = float(nums[0])
    return answer


def simplify(expression):
    global ans

    func = True
    while func == True:
        print(expression)
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
            print(floor, roof, "fr")
            expression = expression[:f - 1] + random(floor, roof) + expression[l + 1:]
        elif "|" in expression:

            f = expression.find("|") + 1
            l = expression.find("|", f)
            num = expression[f:l]

            expression = expression[:f - 1] + abv(simplify(num)) + expression[l + 1:]


        elif "sqrt" in expression:
            f = expression.find("sqrt(") + 5
            l = expression.find(")", f)
            num = expression[f:l]
            print(expression[:f - 5] + num + expression[l + 1:])

            expression = expression[:f - 5] + sqrt(simplify(num)) + expression[l + 1:]
        else:
            func = False
    if func == False:
        return sort(expression)


ans = ""
# while True:
#     ans = simplify(input(""))
#     print("Result: ", ans)




