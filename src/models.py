from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(1600), unique=False, nullable=False)
    image = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Ptoject %r>' % self.name

    def serialize(self):
        return {
            "name": self.name,
            "description": self.description,
            "image": self.image
        }