from flask import Blueprint
from flask_restful import Api
from controllers.Sign_up import RegistrationView


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(RegistrationView, '/auth/signup')
