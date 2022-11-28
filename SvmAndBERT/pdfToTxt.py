import os 
import PyPDF2
import re

# Assign directory
currentDirPath = os.getcwd()
print('Current working directory: ', currentDirPath)
inputDirPath = currentDirPath + '/Syllabi'
ouptutDirPath = currentDirPath + '/SyllabiTxt'


for fileName in os.listdir(inputDirPath):
    f = os.path.join(inputDirPath, "csce482_938.pdf")
    if f[-4:] == '.pdf':                                    # check if it is a pdf file
        if os.path.isfile(f):                               # check if it is a file
            pdfFileObj = open(f, 'rb')                      # create a pdf file obj
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)    # create a pdf reader obj
            numPages = pdfReader.numPages                   # of pages

            print("Converting ", f[len(inputDirPath)+1:], "to txt file")
            
            textFileName = ouptutDirPath + f[len(inputDirPath):-4] + '.txt'

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
                        # if("policy" in w and "attendance" in prev):
                        #     fin = fin[:-11]
                        #     flag = True
                        #     break
                        prev = w
                        fin += w + " "
                txtFile.write(fin)

            pdfFileObj.close()                              # closing the pdf file obj
# break
# print("Conversion Completed!")

