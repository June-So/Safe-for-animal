from app import app, db
from app.utils.scrapping import scrap_data_reviews
from flask import redirect, url_for, request
from app.models import Society, Review

# - ACTION : Remove society from database
@app.route('/admin/remove-society/<society>')
def remove_society(society):
    society = Society.query.get(society)
    db.session.delete(society)
    db.session.commit()
    return redirect(url_for('index'))

# ACTION - Export google review for society in csv and database
@app.route('/admin/scrap-reviews/<society>')
def scrap_reviews(society):
    scrap_data_reviews(society)
    return redirect(url_for('label_data'))

# ---------- AJAX REQUESTS ------------ #

# ACTION [AJAX]: Update review label in database
@app.route('/label-review/<id>', methods=['GET', 'POST'])
def label_review(id):
    review = Review.query.get(id)
    vote = request.args['vote']
    if vote == 'up':
        review.label = True
    elif vote == 'down':
        review.label = False
    db.session.commit()
    return redirect(url_for('label_data'))

# ACTION [AJAX] - remove review from database
@app.route('/remove-review/<id>')
def remove_review(id):
    review = Review.query.get(id)
    db.session.delete(review)
    db.session.commit()
    return 'ok'
