# scikit_hp_tuner
Simplified model for optimising SciKit supervised learners' hyperparameters

## Features
- Tournament-based hyperparameter tuning for Scikit learn's supervised learners
- Supervised prediction for some autoregressive regression models
- Template Abstracted classes for easy creation of custom tuners

## Supports

  Anything in `sklearn.ensemble`. NOTE: Currently I only use RF and GBR. To use anything else, add hyperparameter names to `ALLOWED_PARAMS` in `./lib/hyper_parameter_config.py`
  
  ## Overview
  
   A simple, reaonably abstracted, hyperparameter tuner inspired by [Seyedzadeh et al\(2019)](https://www.researchgate.net/publication/336210712_Multi-Objective_Optimisation_for_Tuning_Building_Heating_and_Cooling_Loads_Forecasting_Models). This model provides a simple way of tuning Scikit-learn supervised learners and designing custom tuners.
   
   Rather than focus on integrating the nondominated sorting GA from the paper, this library is focused on enabling users to create their own scorers and tuners easily.
   
 # Getting started
 
 #### Note: This example is more or less taken from the example script. Run `python ./example.py <target feature> <data csv path>` to try it out.
 
 The model has two noteworthy components needed to get a process running, a `HyperParameterTuner` or descendent and` HyperParemterConfig`s. The former is the main tuner and the latter define the hyperparameter domains.
 
 
#### Example using `sklearn.ensemble.GradientBoostingRegressor`

 ```ruby
 ##
 # Declare model hyperparameters and their domains.
 #
 # Param 1: String hyperparameter name. Must reside in HyperParameterConfig::ALLOWED_PARAMS. Add it if you need it
 # Param 2: Boolean is the parameter type Integer?
 # Param 3: Numeric lower bound hyperparameter value
 # Param 4: Numeric upper bound hyperparameter value
 #
 #  Param 3 <= mutated value <= Param 4
 ##
 hpConfigParams = [
	HyperParameterConfig("random_state", True, 1, 1),
	HyperParameterConfig("n_estimators", True, 500, 2000),
	HyperParameterConfig("learning_rate", False, 0.005, 0.5),
	HyperParameterConfig("min_samples_split", True, 2, 40),
	HyperParameterConfig("min_samples_leaf", True, 2, 20)
]
##
# Set input properites
##
TEST_TRAIN_DATA_PATH  = <Set path to input data containing data for training and 
TARGET                = <Set target field name>
#Input data
data    = pandas.read_csv(TEST_TRAIN_DATA_PATH)
# Sckit-learn supervised learner class 
learnerClass          = GradientBoostingRegressor
##
# Create a tuner and tune a model
#
# Param 1:       `DataFrame` containing all data, training and test. Splitting's dealt with automatically
# Param 2:       `String` target feature/column name
# Param 3:       `Array` of HyperParameterConfig`s which define the solution space
# splitSize:     `flot` test data split size 0 < splitSize < 1 where higher = less training data (Yeah, I know... Too late now)
# maxCacheSize:  `int` Size of the tournament table. Once the size is breached, the tournament begins
# stepLimit:     `int` Number of offspring that can attempt to outperform its parent and be allowed to (This is Sparta!)
# machineClass:  `sklearn-ensemble` learner to create the model. Param 3 needs to have values related to this learner
# cvSize:        `int` k-fold validation, number of partitions
# proofSplitSize:         `float` optional test visible/hidden split. Injects a yellow row letting you see how it would perform if you weren't looking...
# initialPopulationSize:  `int` Starting population size
##
hpTuner =  HyperParameterTuner(data, TARGET, hpConfigParams, splitSize=0.8,
				proofSplitSize=0.6,	maxCacheSize=20, stepLimit=60,
				machineClass=GradientBoostingRegressor,	cvSize=3, initialPopulousSize=12)
hpTuner.run()
```

This will begin printing a poorly formatted table of results and selected hyperparameter values. E.g

![alt text](https://i.imgur.com/YEp1Rmj.png "Logo Title Text 1")

