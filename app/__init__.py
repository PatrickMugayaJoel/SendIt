from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'joelsecret'
jwt = JWTManager(app)

from app.views import views
