import os
import sys
import PyPDF2
import pandas as pd
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, words
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
nltk.download('wordnet')
nltk.download('words')
nltk.download('omw-1.4')
nltk.download('stopwords')


currentDirPath = os.getcwd()

inputDirPath = currentDirPath + '/SyllabiResults'

#reclassify this later
classficationDict = {}
for filename in os.listdir(inputDirPath):
    if filename[:4] == 'Bias':
        classficationDict[filename] = 1
    else:
        classficationDict[filename] = 0


wordSet = set(words.words())
stop_words = set(stopwords.words('english'))

syllabiParsed = []
targetValues = []
for fileName in os.listdir(inputDirPath):
    file = os.path.join(inputDirPath, fileName)
    lemmatizer = WordNetLemmatizer()

    if file[-4:] == '.txt' and os.path.isfile(file):
        targetValues.append(classficationDict[fileName])
        tempDict = set()
        finSyllabus = ""
        with open(file, encoding='utf-8') as f:
            for line in f:
                for word in line.split():
                    if(word.isalpha() and (word in wordSet)):
                        word = word.lower()
                        if(word not in stop_words):
                            finWord = lemmatizer.lemmatize(word)
                            if(finWord not in tempDict):
                                finSyllabus += finWord + " "
                            tempDict.add(finWord)
        syllabiParsed.append(finSyllabus)

tfidf = TfidfVectorizer()

result = tfidf.fit_transform(syllabiParsed)
result = pd.DataFrame(result.toarray())

X = np.array(result)
y = np.array(targetValues)

clf = svm.SVC(probability=True)
clf.fit(X, y)

print("Training Score (accuracy: 1.0 = 100%) = ",end="")
print(clf.score(X,y),"\n")

####################################################################################
# Necessary functions
####################################################################################

# testFileToVec: Convert test txt file to vectors
def testFileToVec(file, tfidf):
    tempDict = set()
    lemmatizer = WordNetLemmatizer()
    finSyllabus = ""
    testFileParased = []
    with open(file, "r") as f:
        for line in f:
            for word in line.split():
                if(word.isalpha() and (word in wordSet)):
                    word = word.lower()
                    if(word not in stop_words):
                        finWord = lemmatizer.lemmatize(word)
                        if(finWord not in tempDict):
                            finSyllabus += finWord + " "
                        tempDict.add(finWord)
    testFileParased.append(finSyllabus)

    result = tfidf.transform(testFileParased)
    result = pd.DataFrame(result.toarray())

    X = np.array(result)
    return X


# getSpamProbability: Get bias probaility 
def getBiasProbability(file, testVec):
    print("Bias test: ", file)
    print("   Answer                          = ", clf.predict(testVec))
    print("   NotBiased vs Biased probability = ", clf.predict_proba(testVec)) 
    if clf.predict(testVec)[0] == 1:
        print(clf.predict(testVec))
        print("It is biased")
    elif clf.predict(testVec)[0] == 0:
        print(clf.predict(testVec))
        print("It is not biased")
    print("")

####################################################################################
# Input PDF -> TXT conversion
####################################################################################

fileName = sys.argv[1]
f = os.path.join(currentDirPath, "inputTestSyllabi", fileName)
ouptutDirPath = currentDirPath + '/inputTestSyllabi/'
print(f)

if f[-4:] == '.pdf' and os.path.isfile(f):          
    if os.path.isfile(f):                               # check if it is a file
        pdfFileObj = open(f, 'rb')                      # create a pdf file obj
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)    # create a pdf reader obj
        numPages = pdfReader.numPages                   # of pages

        print("Converting ", f, "to txt file")
        
        textFileName = ouptutDirPath + filename[:-4] + '.txt'

        flag = False
        fin = ""
        with open(textFileName, 'w') as txtFile:        # create new txt file
            for i in range(numPages):
                text = ""
                # if(i == 0):
                #     continue           
                pageObj = pdfReader.getPage(i)

                if(flag):
                    break  
                for word in pageObj.extract_text():
                    text += word

                for w in text.split():
                    w = w.lower()
                    if("policies" in w and "university" in prev):
                        fin = fin[:-11]
                        flag = True
                        break
                    # if("integs
                    if("with" in w and "americans" in prev):
                        fin = fin[:-10]
                        flag = True
                        break
                    if("policy" in w and "attendance" in prev):
                        fin = fin[:-11]
                        flag = True
                        break
                    prev = w
                    fin += w + " "
            txtFile.write(fin)

        pdfFileObj.close()      
    
print("pdf -> txt Conversion Completed!\n")



####################################################################################
# Print out the result
####################################################################################

# sleep(2)
print(textFileName)
file1 = textFileName
test1 = testFileToVec(file1, tfidf)

# Calculate Bias probability
getBiasProbability(file1, test1)
# os.remove(textFileName)
