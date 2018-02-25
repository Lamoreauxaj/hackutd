from app import db


class Solved(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)
    topic = db.Column(db.String(), nullable=False)
    solvedBy = db.Column(db.String())
    link = db.Column(db.String())
    sourceTitles = db.PickleType()
    sourceLinks = db.PickleType()
