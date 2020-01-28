from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(1600), unique=False, nullable=False)
    image = db.Column(db.String(120), unique=False, nullable=False)
    github = db.Column(db.String(120), unique=True, nullable=True)
    demo = db.Column(db.String(120), unique=True, nullable=True)

    def __repr__(self):
        return '<Project %r>' % self.name

    def serialize(self):
        return {
            "id": self.id, 
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "github": self.github,
            "demo": self.demo
        }

class TechSkills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    skillImage = db.Column(db.String(60), unique=False, nullable=False)

    def __repr__(self):
        return '<TechSkills %r' % self.name
    
    def serialize(self):
        return{
            "id":self.id,
            "name": self.name,
            "skillImage": self.skillImage
        }

class SoftSkills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    skillImage = db.Column(db.String(60), unique=False, nullable=False)

    def __repr__(self):
        return '<TechSkills %r' % self.name
    
    def serialize(self):
        return{
            "id":self.id,
            "name": self.name,
            "skillImage": self.skillImage
        }

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(1000), unique=False, nullable=False)

    def __repr__(self):
        return '<Articles %r' % self.title
    
    def serialize(self):
        return{
            "id":self.id,
            "title": self.title,
            "description": self.description
        }