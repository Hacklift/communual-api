import os
import unittest
import json
from app import create_app, db


class AuthTestCase(unittest.TestCase):
    """Test case for the authenrication blueprint."""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        # initialize the test client
        self.client = self.app.test_client
        # This is the user test json data with a predefined email and password
        self.user_data = {
            "email": "example1@mail.com",
            "password": "password",
            "username": "example1",
            "phone_number": "09067582433"
        }

        with self.app.app_context():
            # Create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_registration(self):
        """Test user registeration works correctly."""
        res = self.client().post('/api/auth/signup', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'], "You registered successfully.")
        self.assertEqual(res.status_code, 201)

    def test_invalid_email_input(self):
        """Test for when user input a wrong email format."""
        self.user_data['email'] = 'example'
        res = self.client().post('/api/auth/signup', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a error message and a 400 status code
        self.assertEqual(result['message'], "Invalid Email Inputed")
        self.assertEqual(res.status_code, 400)

    def test_empty_email_input(self):
        """Test for when a user leave the email field empty."""
        self.user_data['email'] = ''
        res = self.client().post('/api/auth/signup', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a error message and a 400 status code
        self.assertEqual(result['message'], "This field is required.")
        self.assertEqual(res.status_code, 400)

    def test_invalid_password_input(self):
        """Test for when a user input a password lesser than 6 characters"""
        self.user_data['password'] = 'passw'
        res = self.client().post('/api/auth/signup', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a error message and a 400 status code
        self.assertEqual(result['message'],
                         "Password should be greater than 6 characters")
        self.assertEqual(res.status_code, 400)

    def test_invalid_phone_number_input(self):
        """Test for when a user input a phone_number lesser than 8 characters"""
        self.user_data['phone_number'] = '0802347'
        res = self.client().post('/api/auth/signup', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a error message and a 400 status code
        self.assertEqual(result['message'],
                         "Phone number should be greater than 8 characters")
        self.assertEqual(res.status_code, 400)

    def test_invalid_phone_number_input(self):
        """Test for when a user input a phone number that contains any other character apart from numbers """
        self.user_data['phone_number'] = 'this080347653'
        res = self.client().post('/api/auth/signup', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a error message and a 400 status code
        self.assertEqual(result['message'],
                         "Phone numbers must all contain numbers")
        self.assertEqual(res.status_code, 400)

    def test_invalid_username_input(self):
        """Test for when a user input a username lesser than 2 characters"""
        self.user_data['username'] = 'p'
        res = self.client().post('/api/auth/signup', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a error message and a 400 status code
        self.assertEqual(result['message'],
                         "Username should be greater than 2 characters")
        self.assertEqual(res.status_code, 400)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        res = self.client().post('/api/auth/signup', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('/api/auth/signup', data=self.user_data)
        self.assertEqual(second_res.status_code, 409)
        # get the results returned in json format
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['message'], 'Email or phone number is already been used by an existing user. Please try again.')
