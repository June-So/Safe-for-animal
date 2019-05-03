from app import db
import datetime


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_publication = db.Column(db.String(42))
    text = db.Column(db.Text, nullable=False)
    society_id = db.Column(db.Integer, db.ForeignKey('society.id'), nullable=False)
    date_scrap = db.Column(db.String(60), default=str(datetime.datetime.now()))
    label = db.Column(db.Boolean, nullable=True)

    def __init__(self, society, text, date_publication):
        self.text = text
        self.date_publication = date_publication
        self.society = society


class Society(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    reviews = db.relationship('Review', backref='society', cascade="all,delete", lazy=True)

    def __init__(self, name):
        self.name = name


class ScorePrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer, nullable=False)
    count_false = db.Column(db.Integer, nullable=False)
    count_true = db.Column(db.Integer, nullable=False)

    def __init__(self, total):
        self.total = total
        self.count_false = 0
        self.count_true = 0
