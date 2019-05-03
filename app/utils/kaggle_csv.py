from app.models import Review
import pandas as pd


def update_csv_reviews():
    reviews = Review.query.filter(Review.label != None).all()
    texts = [review.text for review in reviews]
    labels = [review.label for review in reviews]
    reviews = pd.DataFrame({"review": texts, "label": labels})
    reviews.to_csv('app/data/kaggle/reviews.csv', index=False)
    return reviews