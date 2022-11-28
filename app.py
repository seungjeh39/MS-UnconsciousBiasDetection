from SvmAndBERT.BERT.bertbiasdetection import GeneralBertBiasDetection
from SvmAndBERT.SVM_Main import SVM
import string
import pickle
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from flask import Flask, render_template, request, url_for
import os, csv
import os.path
import torch.nn as nn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from transformers import BertModel, BertTokenizer, AdamW, get_linear_schedule_with_warmup
from torch.optim import lr_scheduler

import logging
logging.basicConfig(level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore")

# Libraries and retreiving data
import pandas as pd
import matplotlib.pyplot as plt


app = Flask(__name__)

currentDirPath = os.getcwd()

class CompleteModel(nn.Module):
  """
  The model architecture is defined here which is a fully connected layer + normalization on top of a BERT model
  """

  def __init__(self, bert):
    super(CompleteModel, self).__init__()
    self.bert = BertModel.from_pretrained(bert)
    self.drop = nn.Dropout(p=0.25)
    self.out = nn.Linear(self.bert.config.hidden_size, 2) # Number of output classes = 3, positive, negative and N(none)

  def forward(self, ids, mask, token_type_ids):
    _, pooled_output = self.bert(ids, attention_mask=mask, token_type_ids=token_type_ids, return_dict=False)
    output = self.drop(pooled_output)
    return self.out(output)

def ConvertTxtToCsv(text):
    with open(currentDirPath + '/SVMAndBERT/inputTestSyllabi/' + "inputSyllabi.csv", 'w') as out_file:
        writer = csv.writer(out_file, delimiter=",")
        writer.writerow(['id', 'keyword', 'location', 'text'])

        tempString = ""
        ct = 1
            
        for word in text.strip().split():
            if('.' in word):
                if(tempString.lower().__contains__("university policies") or tempString.lower().__contains__("americans with disabilities")):
                    break
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

def ConvertTxtToTxtFile(text):
    with open(currentDirPath + '/SVMAndBERT/inputTestSyllabi/' + "inputSyllabi.txt", 'w') as out_file:
        tempString = ""
        for word in text.strip().split():
            if('.' in word):
                if(tempString.lower().__contains__("university policies") or tempString.lower().__contains__("americans with disabilities")):
                    break
                tempString += " " + word
                out_file.write(tempString)

                tempString = ""
            else:
                tempString += ' ' + word

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    ConvertTxtToCsv(text)
    ConvertTxtToTxtFile(text)

    if request.method == "POST" and text != "":
        GeneralBERTBias = GeneralBertBiasDetection(currentDirPath)
        SVM_BiasProbabilities = SVM(currentDirPath)

        dictionary = ["responsibility","maintain","curve","expect",
                    "expected","expectation","expectations","knowledge",
                    "challenging","earn","prerequisite","ability","own",
                    "experience","recommend","recommended","technical","proficiency",
                    "encourage","encouraged","specific","required","familiarity","assumes",
                    "assume","intensive","required","complex","welcome","introductory"] 
                    #"know","required","complex","welcome","introductory","challenge","complete"

        inputVec = np.array([[0] * len(dictionary)])

        text = text.translate(str.maketrans('', '', string.punctuation))
        for word in text.split():
            word = word.lower()
            if word in dictionary:
                inputVec[0][dictionary.index(word)] = 1


        loadedModel = pickle.load(open('finalizedModel.pkl', 'rb'))
        predictionResult = loadedModel.predict(inputVec)
        biasProbability = loadedModel.predict_proba(inputVec)

        if predictionResult[0] == 1:
            label1 = f'This syllabus is biased according to Naive Bayes Model.'
            label2 = f'NotBiased vs Biased probability (NB) = {biasProbability[0]}'
        elif predictionResult[0] == 0:
            label1 = f'This syllabus is not biased according to Naive Bayes Model.'
            label2 = f'NotBiased vs Biased probability (NB) = {biasProbability[0]}'

        if SVM_BiasProbabilities[0][0] == 1:
            label4 = f'This syllabus is biased according to Support Vector Machine Model.'
            label5 = f'NotBiased vs Biased Probability (SVM) = {SVM_BiasProbabilities[1][0]}'
        elif SVM_BiasProbabilities[0][0] == 0:
            label4 = f'This syllabus is not biased according to Support Vector Machine Model.'
            label5 = f'NotBiased vs Biased Probability (SVM) = {SVM_BiasProbabilities[1][0]}'
        
        label3 = f'BERT General Bias Detection Probability = {GeneralBERTBias}'
        print(GeneralBERTBias)

    else:
        label1, label2, label3, label4, label5 = "", "", "", "", ""

    return(render_template('index.html', NBpredictionTxt=label1, NBprobabilityTxt=label2, BertTxt=label3, SVMpredictionTxt = label4, SVMprobabilityTxt=label5))


if __name__ == "__main__":
    app.debug = True
    app.run(port='5010',threaded=False)
