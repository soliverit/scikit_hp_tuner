import colorama
from colorama import Fore, Style
colorama.init()

class HyperParameterStruct():
	# def senseCheckParams(self):
		# raise "MissingHyperParameterException: missing learn_rate" if not "learn_rate" in self.params
		# raise "MissingHyperParameterException: missing learn_rate" if not "n_esitmators" in self.params
		# raise "MissingHyperParameterException: missing learn_rate" if not "learn_rate" in self.params
	def __init__(self, params, report):
		self.params					= params
		self.report					= report

	@classmethod
	def printHeader(self):
		print("%s\tScorer: %s%s\t" %(Fore.YELLOW, self.SCORER_DESCRIPTION, Style.RESET_ALL))
		print("\tScore\tRMSE\tHyperparameters")
	SCORER_DESCRIPTION = "RMSE (lower is better)"
	def printOut(self, colour=False):
		styleReset = ""
		if colour:
			styleReset	= Style.RESET_ALL
		colour = colour if colour else ""
		print("\t%s%s\t%s\t%s%s" %(colour, round(self.score, 3), self.errorMsg, self.hyperParamterString, styleReset))
	@property
	def hyperParamterString(self):
		output = []
		for key, param in self.params.items():
			param = round(param, 4) if param.__class__ is float else param
			output.append(" %s" %(param))
		return ", ".join(output)
	@property
	def learnRate(self):
		return self.params["learn_rate"]
	@property
	def nEstimators(self):
		return self.params["n_estimators"]
	@property
	def errorMsg(self):
		return round(self.report.RMSE, 3)
	@property
	def score(self):
		return self.report.score
		# return abs(self.rMinRecord.delta - self.rMaxRecord.delta) / abs(self.aMinRecord.delta - self.aMaxRecord.delta)
	@classmethod
	def reduceSet(self, set, limit):
		if len(set) < limit:
			return set
		set.sort(key = lambda a: a.score, reverse = True)
		return set[0:limit]
