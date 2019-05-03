from app import app
from flask import render_template, redirect, request, url_for
from .models import Society, Review
from sqlalchemy import or_

# -- PAGE : Home
@app.route('/', methods=['GET', 'POST'])
def index():
    """ List of all society already scrapp
        RUN : Run scrapp for society by her name from form"""
    societys = Society.query.all()
    if request.method == 'POST':
        society = request.form['society']
        return redirect(url_for('scrap_reviews', society=society))

    return render_template('index.html', societys=societys)

# -- PAGE : Label data
@app.route('/admin/labelliser-donnees', methods=['GET'])
def label_data():
    """ List all reviews in database
        FILTER : Apply filter on label by form """
    reviews = Review.query.all()
    search = request.args.getlist('search')
    print(search)
    if request.method == 'GET' and search:
        print('im in!')
        # #!# Not answer found for apply  1 0 "OR" None conditionnaly at same time
        if 'None' in search:
            search.remove('None')
            reviews = Review.query.filter(or_(Review.label == None, Review.label.in_(search))).all()
        else:
            reviews = Review.query.filter(Review.label.in_(search)).all()
        print(reviews)
    return render_template('data-label.html', reviews=reviews)







