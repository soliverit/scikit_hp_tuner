class ErrorReportRecordBase:
	def __init__(self,inputs, x, y):
		self.inputs		= inputs
		self.x			= x
		self.y			= y
		self.delta		= self.x - self.y

		self.error		= x - y
		self.absError	= abs(x) + abs(y)
		self.se			= self.delta ** 2
	@property
	def target(self):
		return self.x
	@property
	def prediction(self):
		return self.y

