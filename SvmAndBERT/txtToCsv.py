from calendar import c
from lib2to3.pytree import convert
import pandas as pd
import os
import csv
import sys

currentDirPath = os.getcwd()

# class convertTestFile():
#     file = sys.argv[1]
#     with open(currentDirPath + '/SyllabiTxt/' + file, 'r') as in_file:
#         with open(currentDirPath + '/SyllabiCsv/' + file[:-4] + '.csv', 'w') as out_file:
#             writer = csv.writer(out_file, delimiter=",")
#             writer.writerow(['id', 'keyword', 'location', 'text'])

#             tempString = ""
#             ct = 1
#             for line in in_file:
#                 print(line)
#                 if not line.strip():
#                     continue
                
#                 for word in line.strip().split():
#                     if('.' in word):
#                         tempString += " " + word
#                         tempString = tempString.strip()[:-1]
#                         tempList = []

#                         tempList.append(ct)
#                         tempList.append("")
#                         tempList.append("")
#                         tempList.append(tempString)
#                         writer.writerow(tempList)

#                         tempString = ""
#                         ct += 1
#                     else:
#                         tempString += ' ' + word

# convertTestFile()


class convertModelSyllabi:
    for filename in os.listdir(currentDirPath + '/SyllabiTxt'):
        if(".DS" not in filename):
            with open(currentDirPath + '/SyllabiTxt/' + filename, 'r') as in_file:
                with open(currentDirPath + '/SyllabiCsv/' + filename[:-4] + '.csv', 'w') as out_file:
                    writer = csv.writer(out_file, delimiter=",")
                    writer.writerow(['id', 'keyword', 'location', 'text'])

                    tempString = ""
                    ct = 1
                    for line in in_file:
                        if not line.strip():
                            continue
                        
                        for word in line.strip().split():
                            if('.' in word):
                                tempString += " " + word
                                tempString = tempString.strip()[:-1]
                                tempList = []

                                tempList.append(ct)
                                tempList.append("")
                                tempList.append("")
                                tempList.append(tempString)
                                writer.writerow(tempList)

                                tempString = ""
                                ct += 1
                            else:
                                tempString += ' ' + word

convertModelSyllabi()