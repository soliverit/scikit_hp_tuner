from random import randint, shuffle, uniform
import numpy as np
import colorama
from colorama import Fore, Style
from .hyper_parameter_struct import HyperParameterStruct
from .error_report.error_report import ErrorReport
from .error_report.error_report_record import ErrorReportRecord
from sklearn.model_selection import cross_val_score

from sklearn.ensemble import GradientBoostingRegressor

from multiprocessing.dummy import Pool as ThreadPool

import time
class HyperParameterTuner():
	PANIC_MODE = False
	#Should a lower score be considered better?
	DESCENDING_SCORE = True
	###
	# data:		Pandas.DataFrame of all data for tuning, testing and proofing
	# Xtrain:	Training data DataFrame without the target column of len(data) * splitSize
	# Ytrain:	Training targets np.array
	# Xtest:	Test data DataFrame without targets of len(data) * splitSize 
	##
	def __init__(self, data, target, params, 
				splitSize= 0.5, proofSplitSize= 0.5, 
				stepLimit = 40, maxCacheSize=10,
				machineClass=GradientBoostingRegressor,
				cvSize=2,initialPopulousSize=3):

		###
		# Do data splitting
		#
		# Split data into three groups: Train / Test / Proof. Proof is unseen data which
		# is never seen during tuning, a cheating set for working out how you've 
		# done. An initial reality check.
		###
		self.target					= target

		targets					= data[target]
		data					= data.drop(target, 1)		
		
		self.Xtrain				= data[int(len(data) * splitSize):]
		self.Ytrain				= np.array(targets[int(len(data) * splitSize):])
		
		self.Xtest				= data[:int(len(data) * splitSize)]
		self.Ytest				= np.array(targets[:int(len(data) * splitSize)])
		
		##Set up blind data. You can't use this for selecting production models, but it's useful
		self.Xproof 				= self.Xtest[int(len(self.Xtest) * proofSplitSize):]
		self.Xtest 					= self.Xtest[:int(len(self.Xtest) * proofSplitSize)]
		
		self.Yproof					= self.Ytest[int(len(self.Ytest) * proofSplitSize):]
		self.Ytest					= self.Ytest[:int(len(self.Ytest) * proofSplitSize)]
		#Set standard stuff
		self.machineClass		= machineClass
		self.cvSize				= cvSize
		self.stepLimit				= stepLimit
		self.maxCacheSize			= maxCacheSize
		self.hpParameterConfigs		= params
		self.initialPopulousSize	= initialPopulousSize
		
		self.currentSet				= []
		
	def isImprovement(self, baseHP, newHP, ):
		return baseHP.score < newHP.score if not self.__class__.DESCENDING_SCORE else baseHP.score > newHP.score 
	def printOut(self):
		print("\t====== GA ======\n\tTrain size:\t%s\n\tTest size:\t%s\n\tProof size:\t%s\n\tBase population:\t%s\n\tStep limit:\t%s\n\tCache size:\t%s\n\t----------------" %(
			len(self.Xtrain), len(self.Xtest),len(self.Xproof), self.initialPopulousSize, self.stepLimit, self.maxCacheSize
		))
		print(self.targetLabel)
		print("\t--- Hyper parameter configs ---")
		for param in self.hpParameterConfigs:	
			param.printOut()
		print("")
	@property
	def targetLabel(self):
		return "\tTarget:\t%s" %(self.target)
		#return baseHP.acceptCount < newHP.acceptCount or baseHP.error > newHP.error
	def run(self):
		self.printOut()
		best = False
		self.currentSet = []
		#Create initial model ErrorReport from Configs
		print("\t-- Creating initial population of %s" %(self.initialPopulousSize))
		for x in range(self.initialPopulousSize + 1):
			params = {}
			for param in self.hpParameterConfigs:
				params[param.name] 	= param.doMutate()
			tempReport				= self.getError(self.buildModel(params), params, self.Xtest, self.Ytest)
			self.currentSet.append(self.generateParameters(tempReport.hpStruct))
			if not best:
				best			= self.currentSet[0]
				best.hpStruct.__class__.printHeader()
		while True:
			if len(self.currentSet) == 0:
				break
			output			= self.currentSet.pop(0)
			#Pop the first machine from the set
			improvedSet		= self.improve(output)
			for improved in improvedSet:
				best = self.evaluate(best, improved)
				if len(self.currentSet) > self.maxCacheSize:
					currentSet = output.__class__.reduceSet(self.currentSet, self.maxCacheSize)

		report =self.getError(best.model,best.parameters, self.Xproof, self.Yproof)
		report.hpStruct.printOut(Fore.YELLOW)
		return report
	##
	# Evaluate the new ErrorReport and old. Return previous best or improved
	#
	# best:		Current best HyperParameterStruct's ErrorReport
	# improved:	Candidate for the new best HyperParameterStruct's ErrorReport
	#
	# Output:	The best of the two HyperParameterStruct's ErrorReport
	##
	def evaluate(self, best, improved):
		betterThanOne = True
		if self.isImprovement(best, improved):
			best = improved
			improved.hpStruct.printOut(Fore.BLUE)
			if self.cvSize:
				print(cross_val_score(best.model, self.Xtrain, self.Ytrain))
			self.getError(best.model, 
							best.parameters, 
							self.Xproof, 
							self.Yproof).hpStruct.printOut(Fore.YELLOW)
		else:
			#Reduce results to only better than store
			for hpStruct in self.currentSet:
				if self.isImprovement(hpStruct, improved):
					betterThanOne 	= True
				else:
					betterThanOne	= False
			if not betterThanOne:
				improved.hpStruct.printOut(Fore.RED)
			else:
				improved.hpStruct.printOut(Fore.GREEN)
				self.currentSet.append(improved)
		return best
	def improve(self,baseReport):
		output		= []
		t 			= time.time()
		inputs		= [baseReport.hpStruct for x in range(self.stepLimit + 1)]
		pool 		= ThreadPool(4)
		trials		= pool.map(self.generateParameters, inputs)
		pool.close()
		pool.join()
		for newReport in trials:
			if self.isImprovement(baseReport, newReport):
				output.append(newReport)
		# while i < self.stepLimit:
			# #Generate random parameters
			# #Get new HP struct and accept or reject
			# newReport	= self.generateParameters(baseReport.hpStruct)
			# if self.isImprovement(baseReport, newReport):
				# output.append(newReport)
			# i += 1

		return output
	def buildModel(self, parameters):
		model = self.machineClass()
		for k, v in parameters.items():
			setattr(model, k, v)
		model.fit(self.Xtrain, self.Ytrain)
		return model
	def mutateHPConfigs(self, baseHP):
		params	= {}
		trueCount	= 0
		for param in self.hpParameterConfigs:
			if trueCount < len(self.hpParameterConfigs) - 1 and randint(1,100) < 35:
				trueCount += 1
				params[param.name] = param.doMutate()
			else:
				params[param.name] = baseHP.params[param.name]
		return params
	def generateParameters(self, baseHP):
	
		#Generate new model and fit
		parameters	= self.mutateHPConfigs(baseHP)
		model 		= self.buildModel(parameters)
			
		# Print error on training if you're in a panic and think something's wrong
		if self.__class__.PANIC_MODE:
			print("DON'T PANIC (printing prediction on training data)")
			error = self.getError(model, self.Xtrain, self.Ytrain).printOut(Fore.MAGENTA)
			
		#Generate results
		return self.getError(model, parameters, self.Xtest, self.Ytest)
	def getError(self, model, parameters, X, Y):
		report 	= ErrorReport(model, parameters)
		results = model.predict(X)
		i = 0
		for index, row in X.iterrows():
			report.push(ErrorReportRecord(row, Y[i], results[i]))
			i += 1
		return report
