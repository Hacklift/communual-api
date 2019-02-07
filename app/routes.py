from flask import Blueprint
from flask_restful import Api
from controllers.Sign_up import RegistrationView
from controllers.Sign_in import LoginView


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(RegistrationView, '/auth/signup')
api.add_resource(LoginView, '/auth/login')
