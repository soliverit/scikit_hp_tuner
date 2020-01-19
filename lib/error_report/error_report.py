from lib.hyper_parameter_struct import HyperParameterStruct
class ErrorReport:
	REJECT_CONSTRAINT = 0.001
	def __init__(self, model, parameters):
		self.model		= model
		self.parameters	= parameters
		self.records	= []
		self.totalRMSE	= False
	@property
	def hpStruct(self):
		return HyperParameterStruct(self.parameters, self)
	@property
	def score(self):
		return self.RMSE
	def push(self,record):
		self.records.append(record)	
	def append(self, record):
		self.push(record)
	@property
	def RMSE(self):
		rmse = 0
		for record in self.records:
			rmse += record.se
		return (rmse / len(self.records)) ** 0.5
	

	
	def maxTarget(self):
		max = 0
		for record in self.records:
			if record.target > max:
				max = record.target
		return max
	
	########### ORIGINAL REJECTION METHOD ###########
	# @classmethod
	# def reject(self, record):
		# return record.secondarySE > self.REJECT_CONSTRAINT * (record.secondaryTarget / self.maxSecondaryTarget())

	@classmethod
	def toCSV(self, path):
		with open(path, "w") as file:
			file.write("Target,Prediction,Error,Abs Error,Squared Error,Reject,,S-Target,S-Prediction,S-Error\n")
			for record in self.records:
				file.write("%s,%s,%s,%s,%s,%s,,%s,%s,%s,%s" %(
					record.initialTarget,
					record.initialPrediction,
					record.initialError,
					abs(record.initialError),
					abs(record.initialSE),
					str(self.reject(record)),
					record.secondaryTarget,
					record.secondaryPrediction,
					record.secondaryError,
					abs(record.secondaryError)
				) + "\n")

	def summary(self):
		return "x: %2.f, y:%2.f delta: %2.f (%2.f)\t sx: %2.f, sy: %2.f delta: %2.f(%2.f)" %(
			self.x, self.y, self.delta,
			100 -self.x / self.y * 100.0, 
			self.sx, self.sy, self.sDelta,
			100 - self.sx / self.sy * 100.0)