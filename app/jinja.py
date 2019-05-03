from app import app
from app.utils.model_treatment import preprocessing
from sklearn.pipeline import make_pipeline
from lime.lime_text import LimeTextExplainer
from sklearn.externals import joblib
from keras import backend as K


# - JINJA : Return class from review label
@app.context_processor
def to_template():
    def class_label_review(review):
        if review.label == True:
            return 'label-pos'
        elif review.label == False:
            return 'label-neg'
        return ''
    return dict(class_label_review=class_label_review)


# - JINJA :  Load lime for review label
@app.context_processor
def to_template():
    def lime_review(review):
        # ---- LOAD PIPELINE ---- #
        cv = joblib.load("app/data/model/countvectorizer.sav")
        model = joblib.load('app/data/model/opinion_reviews.sav')
        X = review.text
        # ---- PREPROCESSING (one only) ---- #
        X = preprocessing(X)
        # ---- TRAINING PIPELINE ---- #
        c = make_pipeline(cv, model)
        # ---- LIME EXPLAINER ----- #
        class_names = ['negatif', 'positif']
        explainer = LimeTextExplainer(class_names=class_names)
        exp = explainer.explain_instance(X, c.predict_proba, num_features=5)
        K.clear_session()
        return exp.as_html()
    return dict(lime_review=lime_review)