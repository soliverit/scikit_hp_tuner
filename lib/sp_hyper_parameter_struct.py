from .hyper_parameter_struct import HyperParameterStruct

from colorama import Fore, Style
class SpHyperParameterStruct(HyperParameterStruct):
	def __init__(self, parameters, report):
		super(self.__class__, self).__init__(parameters, report)
		
		self.aMaxRecord				= report.maxAcceptedRecord()
		self.aMinRecord				= report.minAcceptedRecord()
		self.rMaxRecord				= report.maxRejectedRecord()
		self.rMinRecord				= report.minRejectedRecord()
		self.acceptCount			= report.acceptedCount()
		self.wrongRejectionCount	= report.wrongRejectionCount()
	SCORER_DESCRIPTION = "Max rejected absolute error / max accepted absolute error (higher is better)"
	@classmethod
	def printHeader(self):
		print("%s\tScorer: %s%s\t" %(Fore.YELLOW, self.SCORER_DESCRIPTION, Style.RESET_ALL))
		print("\tScore\tKept\tReal Error\tRaw Error\t\tHyperparameters")
	def printOut(self, colour=False):
		styleReset = ""
		if colour:
			styleReset	= Style.RESET_ALL
		colour = colour if colour else ""
		print("\t%s%s\t%s\t%s\t%s\t\t%s%s" %(
			colour, round(self.score, 3), self.acceptCount, 
			self.errorMsg, self.rejectedErrorMsg, self.hyperParamterString, styleReset
		))
	
	@property
	def error(self):
		pass
		return abs(self.aMinRecord.delta - self.aMaxRecord.delta)
	@property
	def errorMsg(self):
		return "(%0.f to %0.f)" %(self.aMinRecord.delta, self.aMaxRecord.delta)
	@property
	def rejectedErrorMsg(self):
		return "(%0.f to %0.f)" %(self.rMinRecord.delta, self.rMaxRecord.delta)