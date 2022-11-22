# Biased vs NotBiased Probability Calculation

import os
import sys
import PyPDF2
import pickle
import numpy as np
from sklearn.naive_bayes import MultinomialNB



# Assign directory
currentDirPath = os.getcwd()
print('Current working directory: ', currentDirPath)


####################################################################################
# Dictionary to look up words from the data vector
####################################################################################

dictionary = ["responsibility","maintain","curve","expect",
              "expected","expectation","expectations","knowledge",
              "challenging","earn","prerequisite","ability","own",
              "experience","recommend","recommended","technical","proficiency",
              "encourage","encouraged","specific","required","familiarity","assumes",
              "assume","intensive","required","complex","welcome","introductory"] 
              #"know","required","complex","welcome","introductory","challenge","complete"



####################################################################################
# Training set & Target values
####################################################################################

inputDirPath = currentDirPath + '/SyllabiTxt'

classficationDict = {"csce110_596-599.txt":1,
                     "csce111_500.txt":0,
                     "csce120,121.txt":0,
                     "csce206_500-503.txt":0,
                     "csce206_M01.txt":0,
                     "csce221_200.txt":0,
                     "csce221_500-509.txt":0,
                     "csce221_513-516.txt":0,
                     "csce221_517-520.txt":0,
                     "csce222_203.txt":0,
                     "csce222_501-502.txt":0,
                     "csce222_503.txt":0,
                     "csce222_599.txt":0,
                     "csce310_500.txt":0,
                     "csce312_201,500-503.txt":1,
                     "csce312_504-511.txt":0,
                     "csce312_595-599.txt":0,
                     "csce313_200.txt":1,
                     "csce313_500-599.txt":0,
                     "csce314_500-502.txt":0,
                     "csce314_598-599.txt":0,
                     "csce315_900-907.txt":0,
                     "csce315_908-911,970.txt":0,
                     "csce350_500-503.txt":0,
                     "csce399_500.txt":0,
                     "csce402_500.txt":0,
                     "csce410_501,599.txt":1,
                     "csce411_501.txt":0,
                     "csce411_502.txt":0,
                     "csce411_503.txt":0,
                     "csce420_500.txt":0,
                     "csce421_200,500.txt":0,
                     "csce430_200,500.txt":0,
                     "csce431_500-504.txt":1,
                     "csce433_500.txt":0,
                     "csce435_500.txt":0,
                     "csce436_200,500.txt":0,
                     "csce438_200,500.txt":1,
                     "csce440_500.txt":1,
                     "csce441_200,500.txt":0,
                     "csce443_501.txt":0,
                     "csce445_500.txt":1,
                     "csce446_500.txt":1,
                     "csce451_500.txt":1,
                     "csce462_500-501.txt":0,
                     "csce463_500.txt":0,
                     "csce465_501.txt":0,
                     "csce470_200,500.txt":1,
                     "csce481_599.txt":0,
                     "csce482_931.txt":0,
                     "csce482_932.txt":0,
                     "csce482_933.txt":0,
                     "csce482_934.txt":0,
                     "csce482_935-936.txt":1,
                     "csce482_937.txt":0,
                     "csce482_938.txt":0,
                     "csce483_932.txt":0
                     }


dataset = []
targetValues = []
for fileName in os.listdir(inputDirPath):
    file = os.path.join(inputDirPath, fileName)
    if file[-4:] == '.txt' and os.path.isfile(file):
        targetValues.append(classficationDict[fileName])
        newList = [0] * len(dictionary)
        with open(file,'r') as f:
            print(fileName)
            for line in f:
                for word in line.split():
                    word = word.lower()
                    if word in dictionary:
                        newList[dictionary.index(word)] = 1
        dataset.append(newList)

# dataset (syllabus) vectors
X = np.array(dataset)

# target values (biased=1, unbiased=0)
y = np.array(targetValues)



####################################################################################
# Model set up and training
####################################################################################

clf = MultinomialNB()
clf.fit(X, y)


filename = 'finalizedModel.pkl'
pickle.dump(clf, open(filename, 'wb'))


# Training result
loadedModel = pickle.load(open(filename, 'rb'))
result = loadedModel.score(X,y)
print("Training Score (accuracy: 1.0 = 100%) = ",end="")
print(result,"\n")

