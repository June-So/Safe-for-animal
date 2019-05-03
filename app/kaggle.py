from app import app
from app.utils.kaggle_csv import update_csv_reviews
from flask import flash, redirect, url_for
import os

# - ACTION : Update dataset csv on Kaggle
@app.route('/admin/update-dataset-kaggle')
def update_dataset():
    update_csv_reviews()
    os.system('kaggle datasets version -p app/data/kaggle -m "updated data"')
    flash('csv mis à jour sur kaggle.')
    return redirect(url_for('index'))


@app.route('/admin/import-sav')
def import_sav():
    os.system('kaggle kernels output powpowkow/safe-for-animal -p app/data/model')
    flash('Model importer et mis à jour')
    return redirect(url_for('index'))
