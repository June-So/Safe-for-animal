from app import app, db
from flask import flash, redirect, url_for, render_template
import pandas as pd
from app.utils.model_treatment import preprocessing
from app.models import Review, ScorePrediction
from sklearn.externals import joblib
from keras import backend as K
from app.utils.kaggle_csv import update_csv_reviews

ROOT_FOLDER_KAGGLE = 'app/data/kaggle/'


@app.route('/admin/nettoyer-les-donnees')
def preprocessing_data():
    pathfile = ROOT_FOLDER_KAGGLE + 'reviews_preprocessing.csv'
    data = update_csv_reviews()
    data['review'] = data['review'].apply(preprocessing)
    data.to_csv(pathfile, index=False)
    flash('Les données on été traitées pour le modèle.')
    return redirect(url_for('index'))


# -- ACTION : Predict review with no label
@app.route('/admin/predict-label')
def predict_label():
    # -- Load all review with no label
    reviews = Review.query.filter(Review.label == None).all()
    review_text = [review.text for review in reviews]

    if review_text:
        # ---- LOAD PIPELINE ----
        cv = joblib.load("app/data/model/countvectorizer.sav")
        model = joblib.load('app/data/model/opinion_reviews.sav')
        X = pd.DataFrame({"review": review_text})
        # ---- PREPROCESSING ----- #
        X['review'] = X['review'].apply(preprocessing)
        # ----- WORD EMBEDDING ----- #
        X = cv.transform(X['review'])
        # ---- PREDICTIONS ---- #
        predictions = model.predict(X)
        K.clear_session()
        score = ScorePrediction(len(predictions))
        db.session.add(score)
        db.session.commit()
        # ----- RESULTS ----- #

        results = pd.DataFrame({
            'text': review_text,
            'predict_0': predictions[:, 0],
            'predict_1': predictions[:, 1]
        })
        results.index = [review.id for review in reviews]
        return render_template('includes/predict-label.html', results=results)

    flash('Pas de label à prédire')
    return redirect(url_for('label_data'))

