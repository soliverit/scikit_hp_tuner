class PrintTable():
	def __init__(self, columns):
		self.headers 	= columns
		self.rows		= []
	def addRow(row):
		temp = {}
		for header in self.headers:
			temp.append(str(row[header]) if header in row else "")
		self.rows.append(temp)
	def addAndPrintRow(self, row):
		colLengths = sizeColumns();
		temp		= ""
		for header in self.headers:
		
			temp += str(row[header]) if header in row else ""
		
	def print():
		colLengths 	= sizeColumns()
		headerStrs	= []
		for header in self.headers:
			headerStrs.append(self.pad(header, colLengths[header] + 1)
		print("|".join(headerStrs))
		for row in self.rows:
			row = []
			for header in self.headers:
				row.append(row[header], colLengths[header] + 1)
			print("|".join(row))
		
	def pad(self, input, length):
		while len(input) < length:
			input += " "
		return input
	
	def sizeColumns():
		output = {}
		for header in self.headers:
			output[header] = len(header)
			for row in self.rows:
				if len(row[header]) > output[header]:
					output[header] = len(row[header])
		return output
	

