import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer
from sklearn.feature_extraction.text import CountVectorizer
from keras.utils.np_utils import to_categorical
import spacy

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
import re

nlp = spacy.load('fr')
nltk.download('punkt')
nltk.download('stopwords')


def remove_traduction(text):
    text = text.replace('(traduit par google)', '')
    return re.sub(r'(original).+', '', text)


# Create function using string.punctuation to remove all punctuation
def remove_punctuation(sentence):
    return re.sub(r'[^\w\s]', ' ', sentence)


def remove_stopwords(text):
    stop_words = stopwords.words('french')
    stop_words += ['chien', 'chat', 'avoir', 'être', 'animal', 'pension']
    return np.array([word for word in text if word not in stop_words])


def stemming(text):
    french = FrenchStemmer()
    return np.array([french.stem(word) for word in text])


def lemming(text):
    text_lem = [token.lemma_ for token in nlp(text)]
    return str.join(' ', text_lem)

# ---- PREPROCESSING ---- #
def preprocessing(text):
    text = text.lower()
    text = remove_traduction(text)
    text = remove_punctuation(text)
    text = lemming(text)
    text = word_tokenize(text)
    text = remove_stopwords(text)
    text = " ".join(text)
    return text
