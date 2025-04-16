# library imports
import os

######################################################
# main parameters

debuggingMode = False # False means that things will print normally; True disables "tryPrint()" so only "print()" shows useful for debugging

epochs = 15 # number of times to run the model on random data, averaging the results for better assessment of model accuracy

ratioTrainTest = 0.9 # 0.9 = 90% of data is used for training, 10% is used for testing, 0.8 = 80%-20%, etc

N = 2 # number of previous training instances to consider per chunk (e.g., consider yesterday and the day before if N = 2)

workingMemory = [] # a list or matrix of data that is updated over time by the model (e.g., for MLR, this would be a list with alpha, beta1, beta2, ..., betaN)

daTargetName = "High"

######################################################

# path parameters
projectPath = f'{os.getcwd()}\\'

inputFolderPath = f'{projectPath}input\\'
outputFolderPath = f'{projectPath}output\\'

clDataPath = f'{inputFolderPath}CLData.csv'
daDataPath = f'{inputFolderPath}DAData.csv'
