class matrix():
	
	def __init__(self, list):
		
		self.mtx = self.create(list)
		self.display = self.format(self.mtx)
		self.size = self.getSize(self.mtx)
		self.cols = len(self.mtx[0])
		self.rows = len(self.mtx)


	def format(self,list):
		table = []
		print('list:')
		print(list)
		print('len:'+ str(len(list)))
		for row in list:
			r = ''
			for cell in row:
				r +=str(cell)+' '
				
			r = r[:-1]
			
			table+=[r]
		
		return table

	def getSize(self, trix):
		rows = str(len(trix))
		cols = str(len(trix[0]))
		return "("+rows+","+cols+")"

				
	def create(self,list):

		if type(list) is not str:
			return list
		M = []
		list = list.split('|')
		for row in list:
			row = row.split(',')
			print(row)
			for num in range(len(row)):
				row[num] = int(row[num])
			M.append(row)
		return M
	def multiply(self,b):
		print(90)
		print('b is of type:  '+str(type(b)))
		print('is numeric?'+str(b.isnumeric()))
		if b.isnumeric() is False:
			print("errorrrr")
			
			print('error3')
			
			print("errorrrr1")
			a = self
			b = matrix(b)
			print(type(a),type(b))
			assert a.cols == b.rows
			print("errorrrr2")
			c = [[0 for i in range(b.cols)] for j in range(a.rows)]
			
			for i in range(a.rows):
				for j in range(b.cols):
					for k in range(a.cols):
						c[i][j]+=a.mtx[i][k]*b.mtx[k][j]
			print('end')		
			b = b.display
			
		else:
			print(1)
			a = self
			print(1)
			c = [[0 for i in range(a.cols)] for j in range(a.rows)]
			print(c)
			a = self.mtx
			for row in range(len(a)):
				for cell in range(len(a)):
					c[row][cell] = a[row][cell]*int(b)

			 
		
		a = self.display
		
		return matrix(c).display , a, b , '*'
	def addition(self,b):
		a = self
		c = [[0 for i in range(a.cols)] for j in range(a.rows)]
		for i in range(a.rows):
			for j in range(a.cols):
				c[i][j] = a.mtx[i][j]+b.mtx[i][j]


		return matrix(c).display 
	def subtraction(self,b):
		a = self
		c = [[0 for i in range(a.cols)] for j in range(a.rows)]
		for i in range(a.rows):
			for j in range(a.cols):
				c[i][j] = a.mtx[i][j]-b.mtx[i][j]


		return matrix(c).display 

def isValid(name,m,dic):
	try:
		x = matrix(m)
		
	except:
		return False
	else:
		if dic.get(name,'r') != 'r':
			return False
		return True


def calcMatrix(expression,matrixes):
	inpt = expression
	print(inpt)
	if '*' in inpt:
		x = inpt.find('*')
		a = inpt[:x]
		
		b = matrixes.get(inpt[x+1:])
		if type(b) != str:
			b = inpt[x+1:]
		
		
		try:
			d = 7
			a = matrix(matrixes.get(a))
			print('point', type(a))
			return a.multiply(b)
		except:
			print('Input Error. \nHelp:\nMatrix*num/Matrix')
			return False
	elif '+' in inpt:
		x = inpt.find('+')
		a = inpt[:x]
		b = inpt[x+1:]
		try:
			a = matrix(matrixes.get(a))
			b = matrix(matrixes.get(b))
			assert a.cols == b.cols
			assert a.rows == b.rows
			
		except:
			print('Input Error. \nHelp:\nMatrix+Matrix')
			return False
		else:
			return a.addition(b)
		

	elif '-' in inpt:
		x = inpt.find('-')
		a = inpt[:x]
		b = inpt[x+1:]
		try:
			a = matrix(matrixes.get(a))
			b = matrix(matrixes.get(b))
			assert a.cols == b.cols
			assert a.rows == b.rows
			return a.subtraction(b)
		except:
			print('Input Error. \nHelp:\nMatrix+Matrix')
			return False

		
	else:
		return 'pop'
