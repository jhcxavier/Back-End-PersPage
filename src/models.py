from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String
db = SQLAlchemy()

db = SQLAlchemy()

class User(db.Model):
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id, 
            "name":self.name,
            "email": self.email,
            "password": self.password,
            
        }

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(1600), unique=False, nullable=False)
    image = db.Column(db.String(120), unique=False, nullable=False)
    github = db.Column(db.String(120), unique=True, nullable=True)
    demo = db.Column(db.String(120), unique=True, nullable=True)
    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))

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
    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))

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
    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))

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
    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return '<Articles %r' % self.title
    
    def serialize(self):
        return{
            "id":self.id,
            "title": self.title,
            "description": self.description
        }

class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1600), unique=False, nullable=False)
    image = db.Column(db.String(60), unique=True, nullable=False)
    resume = db.Column(db.String(60), unique=True, nullable=False)
    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return '<About %r' % self.decription
    
    def serialize(self):
        return{
            "id":self.id,
            "description": self.description,
            "image":self.image,
            "resume":self.resume
        }