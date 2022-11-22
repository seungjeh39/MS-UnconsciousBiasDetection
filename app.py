import string
import pickle
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from flask import Flask, render_template, request, url_for


app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']

    if request.method == "POST" and text != "":

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
            label1 = f'This syllabus is biased.'
            label2 = f'NotBiased vs Biased probability = {biasProbability[0]}'
        elif predictionResult[0] == 0:
            label1 = f'This syllabus is not biased.'
            label2 = f'NotBiased vs Biased probability = {biasProbability[0]}'

    else:
        label1, label2 = "", ""

    return(render_template('index.html', predictionTxt=label1, probabilityTxt=label2))


if __name__ == "__main__":
    app.debug = True
    app.run(port='8088',threaded=False)
