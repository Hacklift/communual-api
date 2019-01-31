from flask import request, jsonify
from flask_restful import Resource
from app.models import User


class LoginView(Resource):
    """This class-base handles user login"""

    def post(self):
        """Handle POST request URL -----> /api/auth/login"""
        try:
            # Get the user object using the email (unique to every user)
            email = request.form.get('email').lstrip()
            password = request.form.get('password')

            if email == '' or password == '':
                response = jsonify({
                    'message': 'This field is required.'
                })
                response.status_code = 400
                return response

            user = User.query.filter_by(email=email).first()

            # Try to authenticate the found user using their password
            if user and user.password_is_valid(password):
                # Generate the access token. This will be used as the authorisation header
                access_token = user.generate_token(user.id)
                if access_token:
                    response = jsonify({
                        'message': 'Welcome! You are now logged in.',
                        'access_token': access_token.decode()
                    })
                    response.status_code = 200
                    return response
            else:
                # User does not exist. Therefore, return an error message to the user
                response = jsonify({
                    'message': 'Invalide credentials, Please try again.'
                })
                response.status_code = 401
                return response
        except Exception as e:
            # Create a response containing a string error message
            response = jsonify({
                'message': str(e)
            })
            response.status_code = 500
            return response
