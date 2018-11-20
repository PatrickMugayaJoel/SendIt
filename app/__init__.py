from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import swag_from, Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'joelsecret'
jwt = JWTManager(app)

from app.views import views
