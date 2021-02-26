def identity(size):
    newMtx = [[0 for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            newMtx[i][j] = 1 if j == i else 0
    return matrix(newMtx)


class matrix():
    def __init__(self, l):
        self.mtx = self.createMtx(l)
        self.cols = len(self.mtx[0])
        self.rows = len(self.mtx)

    def isSquare(self):
        return self.cols == self.rows

    def createMtx(self, lst):
        if type(lst) == int:
            return identity(lst)

        assert type(lst) == list, "should be type list"

        sdr = len(lst[0])
        for row in lst:
            assert len(row) == sdr, "rows must all have same length"
            assert type(row) == list, "should be type list"
            for cell in row:
                assert type(cell) == int or float, "matrix must contain numbers"
        return lst

    def det(self):
        try:
            assert self.isSquare()
        except:
            return "Error found. Must use square matrix."
        if len(self) == 1:
            return self.mtx[0][0]
        if len(self) == 4:
            return (self.mtx[0][0] * self.mtx[1][1]) - (self.mtx[0][1] * self.mtx[1][0])
        d = 0
        for c in range(len(self.mtx[0])):
            if c % 2 == 0:  # +
                sign = +1
            else:  # -
                sign = -1

            x = self.mtx[0][c] * sign

            newMtx = []
            for row in range(1, self.rows):
                tab = []
                for col in range(self.cols):
                    if col != c:
                        tab += [self.mtx[row][col]]
                newMtx += [tab]
            newMtx = matrix(newMtx)

            d += x * newMtx.det()
        return d

    def __len__(self):

        return self.rows * self.cols

    def __add__(self, other):
        try:
            assert type(other) == matrix
        except:
            error = "Error found. You can only add by a matrix. Try again"
            return error
        try:
            assert self.rows == other.rows, "the two matrices must have same number of rows"
            assert self.cols == other.cols, "the two matrices must have same number of columns"
        except:
            error = "Error found. Both matrices must be same size. Try Again."
            return error

        newMtx = [[0 for i in range(self.cols)] for j in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                newMtx[i][j] = self.mtx[i][j] + other.mtx[i][j]

        return matrix(newMtx)

    def __sub__(self, other):
        try:
            assert type(other) == matrix
        except:
            error = "Error found. You can only subtract by a matrix. Try again"
            return error
        try:
            assert self.rows == other.rows, "the two matrices must have same number of rows"
            assert self.cols == other.cols, "the two matrices must have same number of columns"
        except:
            error = "Error found. Both matrices must be same size. Try Again."
            return error

        newMtx = [[0 for i in range(self.cols)] for j in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                newMtx[i][j] = self.mtx[i][j] - other.mtx[i][j]

        return matrix(newMtx)

    def __mul__(self, other):
        try:
            assert type(other) == matrix or int or float
        except:
            return  "Error found. Matrix can only be multiplied with object of type int or matrix"
        if type(other) != matrix:
            newMtx = self.mtx.copy()
            for i in range(self.rows):
                for j in range(self.cols):
                    newMtx[i][j] = self.mtx[i][j] * other
            return matrix(newMtx)

        elif type(other) == matrix:
            try:

                assert self.rows == other.cols, "(a*b): matrix a rows sould be equal to matrix b columsn "
            except:
                return "Error found. A*B: matrix A rows should be equal to matrix B columns."
            newMtx = [[0 for i in range(other.cols)] for j in range(self.rows)]

            for i in range(len(self.mtx)):
                for j in range(len(other.mtx[0])):
                    for k in range(len(self.mtx[0])):
                        newMtx[i][j] += self.mtx[i][k] * other.mtx[k][j]

            return matrix(newMtx)

    def __pow__(self, power):
        try:
            assert self.isSquare()
        except:
            return "Error found. Must use square matrix."
        if power == -1:
            return self.inverse()
        if power == 2:
            return self * self
        return self * (self ** (power - 1))


    def __str__(self):
        mString = ""
        for row in self.mtx:
            for cell in row:
                mString += str(cell) + " "
            mString += "\n"
        mString = mString[:-2]
        return mString

    def toList(self):
        lst = []
        for row in self.mtx:
            lst += [row]
        return lst


    def inverse(self):
        try:
            assert self.isSquare()
        except:
            return "Error found. Must use square matrix."
        try:
            assert self.det() != 0
        except:
            return "This matrix does not have inverse because det(M) = 0"

        return self.ajoint() * (1 / self.det())

    def cofactor(self):
        c = [[0 for i in range(self.cols)] for j in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                newMtx = []
                sign = 1 if abs(i - j) % 2 == 0 else -1
                for row in range(self.rows):
                    tab = []
                    for col in range(self.cols):
                        if row != i and col != j:
                            tab += [self.mtx[row][col]]
                    if len(tab) != 0:
                        newMtx += [tab]

                newMtx = matrix(newMtx)
                c[i][j] = newMtx.det() * sign
        return matrix(c)

    def ajoint(self):
        return self.cofactor().transpose()

    def transpose(self):
        newMtx = [[0 for i in range(self.rows)] for j in range(self.cols)]
        for i in range(self.rows):
            for j in range(self.cols):
                newMtx[j][i] = self.mtx[i][j]
        return matrix(newMtx)



"""d = [[1,4],[8,2]]
h = matrix([[4,2]])
d = matrix(d)
print(d-h)"""
