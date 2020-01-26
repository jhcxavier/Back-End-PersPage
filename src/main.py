"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Projects
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

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
        
        project1=Projects(name=body['name'], description=body["description"], image=body['image'])
        db.session.add(project1)
        db.session.commit()
        return 'ok', 200

    if request.method == "GET":
        all_projects = Projects.query.all()
        all_projects = list(map(lambda x: x.serialize(), all_projects))
        return jsonify(all_projects), 200
    # return jsonify(project1), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
