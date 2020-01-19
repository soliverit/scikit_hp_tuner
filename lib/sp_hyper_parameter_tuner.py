from .hyper_parameter_tuner import HyperParameterTuner
from .error_report.sp_error_report import SPErrorReport
from .error_report.sp_error_report_record import SPErrorReportRecord
import pandas
from random import shuffle

from sklearn.ensemble import GradientBoostingRegressor

from colorama import Fore, Style
#####################################################
# Supervised Prediction hyper parameter tuner		#
#													#
# Tune hyper parameters for supervised prediction	#
# models.											#
#####################################################
class SPHyperParameterTuner(HyperParameterTuner):
	DESCENDING_SCORE = False
	###
	# proofSplitSize:	Ratio of data to be used from the test data as proofing / debugging
	##
	def __init__(self, data, target, targets, params, splitSize = 0.5, 
				proofSplitSize = 0.5, stepLimit = 20, 
				maxCacheSize = 20, machineClass=GradientBoostingRegressor,
				initialPopulousSize=8,
				cvSize=3,
				minAcceptRate=0.3):
		super(self.__class__, self).__init__(data, target, params, splitSize,
										proofSplitSize, stepLimit, 
										maxCacheSize, machineClass, cvSize,initialPopulousSize)
		self.targets 		= targets
		self.minAcceptRate 	= minAcceptRate
	@property
	def targetLabel(self):
		return "\tTargets:\t%s" %(" ".join(self.targets))
	def isImprovement(self, baseHP, newHP, ):
		if len(newHP.acceptedSet) < len(newHP.records) * self.minAcceptRate:
			return False
		return baseHP.score < newHP.score if not self.__class__.DESCENDING_SCORE else baseHP.score > newHP.score 
	def getError(self, model, hpParameters, X, Y):
		outputs 	= model.predict(X)
		newTests 	= pandas.DataFrame(columns=X.columns)
		newTargets	= []
		errs		= []
		i 			= -1
		for index, row in X.iterrows():	
			i					+= 1
			potentialTargets	= []
			currentTargetlabel	= False 
			for target in self.targets:
				if row[target] == -1:
					currentTargetlabel = target
				else:
					potentialTargets.append(target)
			#Inject prediction
			row[currentTargetlabel] = outputs[i]
			#Choose and define a new target
			shuffle(potentialTargets)
			for pt in potentialTargets:
				if row[pt] != 0:
					newTargets.append(row[pt])
					row[pt]				= -1
					newTests = newTests.append(row)
					break
		#Do substituted prediction and create ErrorReport
		newPredictions	= model.predict(newTests)
		report			= SPErrorReport(model, hpParameters)
		i 				= 0
		for index, row in newTests.iterrows():
			report.push(SPErrorReportRecord(row,  Y[i], outputs[i], newPredictions[i], newTargets[i]))
			i += 1
		return report
		
		
		