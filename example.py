################################################
# Native includes: Might be needed, might not...
from colorama import init, Fore, Style
import numpy as np
import os
import pandas
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, make_scorer
import sys
init()
################################################
from lib.sp_hyper_parameter_tuner import SPHyperParameterTuner
from lib.hyper_parameter_tuner import HyperParameterTuner
from lib.hyper_parameter_struct import HyperParameterStruct
from lib.hyper_parameter_config import HyperParameterConfig

print("""
##
# Hyperband hyperparameter tuning for Scikit-learn
#
# The tuner is a tournament-based genetic algorithm
# which attempts to find optimal hyperparameter values
# for supervised learners.
#
# Supervised prediction:
#
#	Some autoregressive models have the neat feature of features
#	whose unit type is the same as the target feature. When this
#	is the case predictions from a trained model can be supervised to an extent. 
#
#	Say for example, you've a four features, Age, Sex, Salary and 
#	AnnualPensionContributions. Salary and PensionContributions share
#	the same unit £/year and are known to be related so they can supervise
#	one another's prediction. This is achieved by simply nulling the target 
#	column in the test data and setting its the training target as the nulled
#	value. Say we have two records and the target is Salary
#
#	id	Age	Sex	Salary	AnnualPensionContributions
#	 1	 25	 1	30000	 804
#	 2 	 40	 0	45000	 1242
#
# 	If they became training data, there'd be up to training records:
#
#	id	Age	Sex	Salary	AnnualPensionContributions	Target
#	 1	 25	 1	-1		 804						 30000
#	 2 	 40	 0	-1		 1242						 45000	
#	 1	 25	 1	30000	 -1							 804
#	 2 	 40	 0	45000	 -1							 1242
#
#	Our model is trained on these then when a prediction is requested
#	say:
#
#	id	Age	Sex	Salary	AnnualPensionContributions
#	 1	 25	 1	-1		 1002
#
# 	Both of the following predictions are made
#
#	data				= myData.getByID(1)
#	Y^1 				= Model.predict(myData.getByID(1))
#	secondPrediction	= {Age:25, Sex:1, Salary: Y^1, AnnualPensionContributions:-1}
#	Y^2					= Model.predict(secondPrediction)
#
#	Now you can compare Y^2 to data.AnnualPensionContributions. If
#	it's not reasonably close, then your first prediction is probably
#	wrong.
#	
# Modes:
#
#	The model has two modes, "standard" and "sp" for normal
#	and autoregressive "supervised prediction". Passed as parameter ARG 3
#
#
##
""")
hpConfigParams = [
	HyperParameterConfig("random_state", True, 1, 1),
	HyperParameterConfig("n_estimators", True, 500, 2000),
	HyperParameterConfig("learning_rate", False, 0.005, 0.5),
	HyperParameterConfig("min_samples_split", True, 2, 40),
	HyperParameterConfig("min_samples_leaf", True, 2, 20)
]
##
# Make sure a target has been passed
##
if len(sys.argv) < 2:
	print("Error: Missing target feature name as arg 1")
	exit()
##
# Make sure input data path was passed and exists
##
if len(sys.argv) < 3 or not os.path.exists(sys.argv[2]):
	print("Error: Input data path either not defined (ARGV 2) or doesn't exist")
	exit()

##
# Set properties
##
target	= sys.argv[1]
data 	= pandas.read_csv(sys.argv[2]).sample(frac=1)

##
# Either do standard or supervised prediction. IF sp do supervised
##
if len(sys.argv) >= 4 and sys.argv[3] == "sp":

	hpTuner = SPHyperParameterTuner(data, target, sys.argv[4].split(","),
		hpConfigParams,	maxCacheSize=30, stepLimit=100, 
		machineClass=GradientBoostingRegressor,	cvSize=3, initialPopulousSize=5)
else:
	hpTuner =  HyperParameterTuner(data, target, hpConfigParams, splitSize=0.8,
				proofSplitSize=0.6,	maxCacheSize=20, stepLimit=60,
				machineClass=GradientBoostingRegressor,	cvSize=3, initialPopulousSize=12)
hpTuner.run()



