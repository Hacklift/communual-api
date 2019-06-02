import os
from app import db
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from database.config import Config


class User(db.Model):
    """This class defines the users table """

    __tablename__ = 'users'

    # Define the columns of the users table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    username = db.Column(db.String(256), nullable=False, unique=True)
    firstname = db.Column(db.String(256), nullable=True)
    lastname = db.Column(db.String(256), nullable=True)
    password = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(256), nullable=False, unique=True)
    registered_on = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, email, password, phone_number, firstname, lastname, username):
        """Initialize the user with an email and a password."""
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.phone_number = phone_number
        self.username = username
        self.firstname = firstname
        self.lastname = lastname

    def generate_password_hash(self, password):
        """
        Generate a password hash from the password provided
        """
        psw_hash = Bcrypt().generate_password_hash(password)

        return psw_hash

    def check_password_validation(self, psw_hash, password):
        """
        Check the validity of the password against the one provided by the user
        """
        check_password = Bcrypt().check_password_hash(psw_hash, password)
        return check_password

    def save(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=30),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key

            jwt_string = jwt.encode(
                payload,
                os.getenv('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)
