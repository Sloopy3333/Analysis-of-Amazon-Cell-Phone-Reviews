from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import numpy as np
import random
import re
import pandas as pd
import string
from nltk.corpus import stopwords
from sklearn.utils import shuffle
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
import pickle
global graph
model = load_model('D:\ML\Amazon_review\model.h5')
cv = pickle.load(open('D:\ML\Amazon_review\cv_vac.pickle', 'rb'))


def predictor(word):
    words = []
    for i in word:
        X = i
        ps = PorterStemmer()
        X = re.sub('[^a-zA-Z]', ' ', X)
        X = X.lower()
        X = X.split()
        X = [ps.stem(w) for w in X if not w in stopwords.words('english')]
        X = ' '.join(X)
        words.append(X)
    X_in = cv.transform(word).toarray()
    pred = np.array(model.predict_classes(X_in))
    if pred > 0.65:
        my_pred = 'Positive review'
    else:
        my_pred = 'negetive review '
    return my_pred


app = Flask(__name__, template_folder=r'D:\ML\Amazon_review\server\template')


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/prediction', methods=["POST"])
def prediction():
    word = request.form['review']
    prediction = predictor([word])
    return render_template('result.html', my_prediction=prediction)


if __name__ == '__main__':
    app.run(debug=False)
