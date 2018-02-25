import app


class Unsolved(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    title = app.db.Column(app.db.String(), unique=True, nullable=False)
    topic = app.db.Column(app.db.String(), nullable=False)
    solvability = app.db.Column(app.db.Float())
    link = app.db.Column(app.db.String())
    sourceTitles = app.db.Column(app.db.PickleType())
    sourceLinks = app.db.Column(app.db.PickleType())
