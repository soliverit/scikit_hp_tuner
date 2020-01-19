from random import randint, uniform
class HyperParameterConfig():
	ALLOWED_PARAMS = ["min_samples_leaf", "min_samples_split","random_state", "learning_rate", "n_estimators", "min_sample_leaf"]
	def __init__(self, name, isInt, min, max):
		if name not in self.__class__.ALLOWED_PARAMS:
			print(name)
			exit()
			raise "HPConfigInvalidParameterException: %s is not a valid hyper parameter" %(name)
		self.name 	= name
		self.min 	= min
		self.max	= max
		self.isInt	= isInt
	def printOut(self, tabString = "\t"):
		print("%sName: %s%sMin:%s\tMax:%s\tInteger?:\t%s" %(tabString, self.name,tabString, self.min, self.max, self.isInt))
	def doMutate(self):
		return randint(self.min, self.max) if self.isInt else uniform(self.min, self.max)
