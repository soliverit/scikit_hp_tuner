from .error_report import ErrorReport
from lib.sp_hyper_parameter_struct import SpHyperParameterStruct
class SPErrorReport(ErrorReport):
	def __init__(self, model, parameters, rejectByInitialPrediction = False):
		super(self.__class__, self).__init__(model, parameters)
		
		self.rejectByInitialPrediction		= rejectByInitialPrediction
		
		self.absAvgAcceptedError			= 0
		self.absAvgRejectedError			= 0
		self.avgAcceptedError				= 0
		self.avgRejectedError				= 0
		
		self.acceptedRMSE					= False
		self.rejectedRMSE					= False
		
		self.rejectedSet 					= []
		self.wronglyRejectedSet				= []
		
		self.acceptedSet					= []
		self.wronglyAcceptedSet				= []
		
		self.acceptedByInitialSet			= []
		self.acceptedBySecondarySet			= []
		
		self.correctlyRejectedByInitialSet	= []
		self.correctlyAcceptedByInitialSet	= []
		
		self.correctlyRejectedBySecondSet	= []
		self.correctlyAcceptedBySecondSet	= []
		
		self.WronglyRejectedByInitialSet	= []
		self.WronglyAcceptedByInitialSet	= []
		
		self.WronglyRejectedBySecondSet		= []
		self.WronglyAcceptedBySecondSet		= []
	@property
	def hpStruct(self):
		return SpHyperParameterStruct(self.parameters, self)
	@property
	def score(self):	
		#return self.sRMSE(True)
		lowHighAccepted = self.lowHighRejected()
		return ((abs(lowHighAccepted["initial"]["min"].delta) + 
				abs(lowHighAccepted["initial"]["max"].delta)) /
				(abs(lowHighAccepted["second"]["min"].sDelta) +
				abs(lowHighAccepted["second"]["max"].sDelta)))
	def lowHighRejected(self):
		output = {"initial": {"min": False, "max": False}, "second": {"min": False, "max": False}}
		for record in self.records:
			if self.reject(record):
				if not output["second"]["min"] or record.sDelta < output["second"]["min"].sDelta:
					output["second"]["min"] = record
				elif not output["second"]["max"] or record.sDelta > output["second"]["max"].sDelta:
					output["second"]["max"] = record
			if self.reject(record, True):
				if not output["initial"]["min"] or record.delta < output["initial"]["min"].delta:
					output["initial"]["min"] = record
				elif not output["initial"]["max"] or  record.delta > output["initial"]["max"].delta:
					output["initial"]["max"] = record
		return output
	def maxSecondaryTarget(self):
		max = 0
		for record in self.records:
			if record.sy > max:
				max = record.sy
		return max
	def reject(self, record, useInitial = False):
		if useInitial:
			return abs(self.maxTarget() * record.delta / record.x ** 2) > self.REJECT_CONSTRAINT	
		return abs(self.maxSecondaryTarget() * record.sDelta / record.sx ** 2) > self.REJECT_CONSTRAINT
	def RMSE(self,withRejection=False):
		rmse = 0
		for record in self.records:
			if withRejection and self.reject(record):
				continue
			rmse += record.initialSE
		return (rmse / len(self.records)) ** 0.5
	def sRMSE(self,withRejection=False):
		rmse = 0
		for record in self.records:
			if not(withRejection and self.reject(record)):
				rmse += record.sse
		return (rmse / len(self.records)) ** 0.5
	# def printThis(self):
		# accepted 	= self.maxAcceptedRecord()
		# rejected	= self.maxRejectedRecord()
		# print("\n\tCount: accepted %s of %s (%s)" %(
			# self.acceptedCount(),
			# len(self.records),
			# round(self.acceptedCount() / len(self.records) * 100,2))
		# )
		# print("\tRMSE: accepted: %2.f\t all: %2.f" %(
			# self.RMSE(True), 
			# self.RMSE(False))
		# )
		# print("\tMAE accepted: %2.f\t rejected: %2.f" %(
			# self.maeAccepted(),
			# self.maeRejected()
		# ))
		# print("\tAvg accepted: %2.f\t rejected: %2.f" %(
			# self.avgAccepted(),
			# self.avgRejected()
		# ))
		# print("\tMax accepted: %2.f\t rejected: %2.f" %(
			# accepted.delta,
			# rejected.delta
		# ))
		
		# print("\n=== Records ===")
		# print("\tAccepted: " + accepted.summary())
		# print("\tRejected: " + rejected.summary())

	# def maxAcceptedError(self):
		# error	= 0
		# for record in self.records:
			# if not self.reject(record) and abs(record.initialError) > error:
				# error = abs(record.initialError)
		# return error
	# def maeAccepted(self):
		# error	= 0
		# count	= 0
		# for record in self.records:
			# if not self.reject(record):
				# error += abs(record.initialError)
				# count += 1
		# return error / count
	def avgAccepted(self):
		error	= 0
		count	= 0
		for record in self.records:
			if not self.reject(record):
				error += record.initialError
				count += 1
		return error / count
	def avgRejected(self):
		error	= 0
		count	= 0
		for record in self.records:
			if self.reject(record):
				error += record.initialError
				count += 1
		return error / count
	def maeRejected(self):
		error	= 0
		count	= 0
		for record in self.records:
			if self.reject(record):
				error += abs(record.initialError)
				count += 1
		return error / count
	def maxRejectedError(self):
		error	= 0
		for record in self.records:
			if self.reject(record) and abs(record.initialError) > error:
				error = record.initialError
		return error
	def acceptedCount(self):
		i = 0
		for record in self.records:
			if not self.reject(record):
				i += 1
		return i
	def wrongRejectionCount(self):
		count = 0
		for record in self.records:
			if self.reject(record) and not self.reject(record, True):
				count += 1
		return count
	def absAvgWronglyRejectedError(self):
		count 	= 0
		error	= 0
		for record in self.records:
			if self.reject(record) and not self.reject(record, True):
				count += 1
				error += record.absError
		return error / count
	def maxAcceptedRecord(self):

		output 	= False
		max		= -999999
		for record in self.records:
			if not self.reject(record) and record.delta > max:
				max = record.delta
				output = record
		return output
	def minAcceptedRecord(self):
		output 	= False
		min		= 9999999999
		for record in self.records:
			if not self.reject(record) and record.delta < min:
				min = record.delta
				output = record
		return output
	def maxRejectedRecord(self):
		output 	= False
		max		= -99999999
		for record in self.records:
			if self.reject(record) and record.delta > max:
				max = abs(record.delta)
				output = record
		return output
	
	def minRejectedRecord(self):
		output 	= False
		min		= 99999999999
		for record in self.records:
			if self.reject(record) and record.delta < min:
				min = record.delta
				output = record
		return output
	def push(self, record):
		#Initial
		if self.reject(record):
			
			self.absAvgRejectedError *= len(self.rejectedSet) + abs(record.sDelta) / (len(self.rejectedSet) + 1)
			self.rejectedSet.append(record)
			if not self.reject(record, True):
				self.wronglyRejectedSet.append(record)
			else:
				self.correctlyRejectedBySecondSet.append(record)
		else:
			self.absAvgAcceptedError *= len(self.rejectedSet) + abs(record.sDelta) / (len(self.rejectedSet) + 1)
			self.acceptedSet.append(record)
				##### TODO: Other caching stuff for wrong accepted 
		if self.reject(record, True) is True:
			self.rejectedSet.append(record)
			if not self.reject(record):
				self.wronglyRejectedByInitialSet.append(record)
			else:
				self.correctRejectionsBySecondSet.append(record)
		else:
			self.acceptedByInitialSet.append(record)
		self.records.append(record)