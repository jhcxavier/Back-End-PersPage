"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
# from os import environ
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Projects, TechSkills, SoftSkills, Articles, About, User
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY') 
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

################################################
# JWT
################################################
# Setup the Flask-JWT-Simple extension for example


# Provide a method to create access tokens. The create_jwt()
# function is used to actually generate the token
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)

    if not email:
        return jsonify({"msg": "Missing email in request"}), 400
    if not password:
        return jsonify({"msg": "Missing password in request"}), 400

    # check for user in database
    usercheck = User.query.filter_by(email=email, password=password).first()

    # if user not found
    if usercheck == None:
        return jsonify({"msg": "Invalid credentials provided"}), 401

    #if user found, Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=email)}
    return jsonify(ret), 200

################################################
# USER METHODS
################################################
#POST AND GET
@app.route('/user', methods=['POST', 'GET'])
def handle_user():

        #POST method
    if request.method == "POST":
        body = request.get_json()
        #Conditions for request!
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if "email" not in body:
            raise APIException('You need to specify the email', status_code=400)
        if "password" not in body:
            raise APIException('You need to specify the password', status_code=400)
        
        user1 = User(email = body['email'], password = body["password"])
        db.session.add(user1)
        db.session.commit()

        return 'ok', 200

        #GET Method
    if request.method == 'GET':
        all_users = User.query.all()
        all_users = list(map(lambda x: x.serialize(), all_users))
        return jsonify(all_users), 200

#PUT, GET AND DELETE
@app.route("/user/<int:user_id>", methods=["PUT", "GET", "DELETE"])
def handle_single_user(user_id):

    # PUT Method

    if request.method == "PUT":
        body = request.get_json(user_id)

        if body is None:
            raise APIException('You need to specify the request body as a json object', status_code = 400)
        
        user = User.query.get(user_id)
        if "email" in body:
            user.email = body['email']
        if 'password' in body:
            user.password = body['password']
        
        db.session.commit()

        return jsonify(user.serialize()), 200

    # GET Method

    if request.method == 'GET':
        all_users = User.query.all()
        all_users = list(map(lambda x: x.serialize(), all_users))
        return jsonify(all_users), 200

    # DELETE Method

    if request.method == 'DELETE':
        user = User.query.get(user_id)
        if user is None:
            raise APIException('User not found', status_code=400)
        db.session.delete(user)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404


################################################
# PROJECTS METHODS
################################################
@app.route('/projects', methods=['POST', 'GET'])
def handle_projects():

    if request.method =='POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if "name" not in body:
            raise APIException('You need to specify the name', status_code=400)
        if "description" not in body:
            raise APIException('You need to specify the description', status_code=400)
        if "image" not in body:
            raise APIException('You need to specify the images', status_code=400)
        if "github" not in body:
            raise APIException('You need to specify the github address', status_code=400)
        if "demo" not in body:
            raise APIException('You need to specify the demo\'s link')
        
        project1=Projects(name=body['name'], description=body["description"], image=body['image'], github=body['github'], demo=body['demo'])
        db.session.add(project1)
        db.session.commit()
        return 'ok', 200

    if request.method == "GET":
        all_projects = Projects.query.all()
        all_projects = list(map(lambda x: x.serialize(), all_projects))
        return jsonify(all_projects), 200
    # return jsonify(project1), 200

@app.route('/projects/<int:project_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_project(project_id):

    # PUT Method

    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        
        project1 = Projects.query.get(project_id)
        if "name" in body:
            project1.name = body['name']
        if 'description' in body:
            project1.description = body['description']
        if 'image' in body:
            project1.image = body['description']
        if 'github' in body:
            project1.github = body['github']
        if 'demo' in body: 
            project1.demo = body['demo']
        db.session.commit()

        return jsonify(project1.serialize()), 200
    

    # GET Method

    if request.method == "GET":
        all_projects = Projects.query.all()
        all_projects = list(map(lambda x: x.serialize(), all_projects))
        return jsonify(all_projects), 200

    # DELETE Method

    if request.method == "DELETE":
        project1 = Projects.query.get(project_id)
        if project1 is None:
            raise APIException('User not found', status_code=400)
        db.session.delete(project1)
        db.session.commit()
        return "ok", 200
    
    return "Invalid method", 404

################################################
# TECH SKILLS METHODS
################################################

#POST AND GET
@app.route('/techskills', methods=['POST', 'GET'])
def handle_techskills():

        #POST method
    if request.method == "POST":
        body = request.get_json()
        #Conditions for request!
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if "name" not in body:
            raise APIException('You need to specify the name', status_code=400)
        if "skillImage" not in body:
            raise APIException('You need to specify the skillImage', status_code=400)
        
        skills = TechSkills(name = body['name'], skillImage = body["skillImage"])
        db.session.add(skills)
        db.session.commit()

        return 'ok', 200

        #GET Method
    if request.method == 'GET':
        all_skills = TechSkills.query.all()
        all_skills = list(map(lambda x: x.serialize(), all_skills))
        return jsonify(all_skills), 200

#PUT, GET AND DELETE
@app.route("/techskills/<int:skill_id>", methods=["PUT", "GET", "DELETE"])
def handle_single_skill(skill_id):

    # PUT Method

    if request.method == "PUT":
        body = request.get_json(skill_id)

        if body is None:
            raise APIException('You need to specify the request body as a json object', status_code = 400)
        
        skills = TechSkills.query.get(skill_id)
        if "name" in body:
            skills.name = body['name']
        if 'skillImage' in body:
            skills.skillImage = body['skillImage']
        
        db.session.commit()

        return jsonify(skills.serialize()), 200

    # GET Method

    if request.method == 'GET':
        all_skills = TechSkills.query.all()
        all_skills = list(map(lambda x: x.serialize(), all_skills))
        return jsonify(all_skills), 200

    # DELETE Method

    if request.method == 'DELETE':
        skills = TechSkills.query.get(skill_id)
        if skills is None:
            raise APIException('User not found', status_code=400)
        db.session.delete(skills)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

################################################
# SOFT SKILLS METHODS
################################################

#POST AND GET
@app.route('/softskills', methods=['POST', 'GET'])
def handle_soft_skills():

        #POST method
    if request.method == "POST":
        body = request.get_json()
        #Conditions for request!
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if "name" not in body:
            raise APIException('You need to specify the name', status_code=400)
        if "skillImage" not in body:
            raise APIException('You need to specify the skillImage', status_code=400)
        
        skills = SoftSkills(name = body['name'], skillImage = body["skillImage"])
        db.session.add(skills)
        db.session.commit()

        return 'ok', 200

        #GET Method
    if request.method == 'GET':
        all_skills = SoftSkills.query.all()
        all_skills = list(map(lambda x: x.serialize(), all_skills))
        return jsonify(all_skills), 200

#PUT, GET AND DELETE
@app.route("/softskills/<int:skill_id>", methods=["PUT", "GET", "DELETE"])
def handle_single_soft_skill(skill_id):

    # PUT Method

    if request.method == "PUT":
        body = request.get_json(skill_id)

        if body is None:
            raise APIException('You need to specify the request body as a json object', status_code = 400)
        
        skills = SoftSkills.query.get(skill_id)
        if "name" in body:
            skills.name = body['name']
        if 'skillImage' in body:
            skills.skillImage = body['skillImage']
        
        db.session.commit()

        return jsonify(skills.serialize()), 200

    # GET Method

    if request.method == 'GET':
        all_skills = SoftSkills.query.all()
        all_skills = list(map(lambda x: x.serialize(), all_skills))
        return jsonify(all_skills), 200

    # DELETE Method

    if request.method == 'DELETE':
        skills = SoftSkills.query.get(skill_id)
        if skills is None:
            raise APIException('User not found', status_code=400)
        db.session.delete(skills)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404

################################################
# ARTICLES METHODS
################################################

#POST AND GET
@app.route('/articles', methods=['POST', 'GET'])
def handle_articles():

        #POST method
    if request.method == "POST":
        body = request.get_json()
        #Conditions for request!
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if "title" not in body:
            raise APIException('You need to specify the title', status_code=400)
        if "description" not in body:
            raise APIException('You need to specify the description', status_code=400)
        
        article = Articles(title = body['title'], description = body["description"])
        db.session.add(article)
        db.session.commit()

        return 'ok', 200

        #GET Method
    if request.method == 'GET':
        all_articles = Articles.query.all()
        all_articles = list(map(lambda x: x.serialize(), all_articles))
        return jsonify(all_articles), 200

# PUT, GET AND DELETE
@app.route("/articles/<int:articles_id>", methods=["PUT", "GET", "DELETE"])
def handle_single_article(articles_id):

    # PUT Method

    if request.method == "PUT":
        body = request.get_json(articles_id)

        if body is None:
            raise APIException('You need to specify the request body as a json object', status_code = 400)
        
        article = Articles.query.get(articles_id)
        if "title" in body:
            article.title = body['title']
        if 'description' in body:
            article.description = body['description']
        
        db.session.commit()

        return jsonify(article.serialize()), 200

    # GET Method

    if request.method == 'GET':
        all_articles = SoftSkills.query.all()
        all_articles = list(map(lambda x: x.serialize(), all_articles))
        return jsonify(all_articles), 200

    # DELETE Method

    if request.method == 'DELETE':
        article = Articles.query.get(articles_id)
        if article is None:
            raise APIException('User not found', status_code=400)
        db.session.delete(article)
        db.session.commit()
        return "ok", 200

################################################
# ABOUT METHODS
################################################

#POST AND GET
@app.route('/about', methods=['POST', 'GET'])
def handle_about():

        #POST method
    if request.method == "POST":
        body = request.get_json()
        #Conditions for request!
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if "description" not in body:
            raise APIException('You need to specify the description', status_code=400)
        if "image" not in body:
            raise APIException('You need to specify the image', status_code=400)
        if "resume" not in body:
            raise APIException('You need to specify the resume', status_code=400)
        
        # about = About(description = body["description"])
        db.session.add(About(description = body["description"], image= body['image'], resume=body["resume"]))
        db.session.commit()

        return 'ok', 200

        #GET Method
    if request.method == 'GET':
        all_about = About.query.all()
        all_about = list(map(lambda x: x.serialize(), all_about))
        return jsonify(all_about), 200

# PUT, GET AND DELETE
@app.route("/about/<int:about_id>", methods=["PUT", "GET", "DELETE"])
def handle_single_about(about_id):

    # PUT Method

    if request.method == "PUT":
        body = request.get_json(about_id)

        if body is None:
            raise APIException('You need to specify the request body as a json object', status_code = 400)
        
        about = About.query.get(about_id)
        if "title" in body:
            about.title = body['title']
        if 'description' in body:
            about.description = body['description']
        if 'image' in body:
            about.image = body['image']
        if 'resume' in body:
            about.resume = body['resume']
        
        db.session.commit()

        return jsonify(about.serialize()), 200

    # GET Method

    if request.method == 'GET':
        all_about = About.query.all()
        all_about = list(map(lambda x: x.serialize(), all_about))
        return jsonify(all_about), 200

    # DELETE Method

    if request.method == 'DELETE':
        about = About.query.get(about_id)
        if about is None:
            raise APIException('User not found', status_code=400)
        db.session.delete(about)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
