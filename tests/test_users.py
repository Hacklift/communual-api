import os
import unittest
import json
from app import create_app, db
from database.db_models.user_models import User


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
            "phone_number": "09067582433",
            "confirm_password": 'password'
        }

        with self.app.app_context():
            # Create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

            user_1 = User(email="example3@mail.com", password="password", username="example3",
                          phone_number="09067582999", firstname='', lastname='')

            user_1.save()

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

    # Login test
    def test_user_login(self):
        """Test registered user can login."""
        self.user_login_data = {
            'email': 'example3@mail.com',
            'password': 'password'
        }
        login_res = self.client().post('/api/auth/login', data=self.user_login_data)

        # get the results in json format
        result = json.loads(login_res.data.decode())

        # Test that the response contains success message
        self.assertEqual(result['message'], "Welcome! You are now logged in.")
        # Assert that the status code is equal to 200
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_invalid_user_login_input(self):
        """Test if email field is empty"""
        res = self.client().post('/api/auth/signup', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        self.user_data['email'] = ''
        login_res = self.client().post('/api/auth/login', data=self.user_data)

        # get the results in json format
        result = json.loads(login_res.data.decode())
        # Test that the response contains success message
        self.assertEqual(result['message'], "This field is required.")
        # Assert that the status code is equal to 400
        self.assertEqual(login_res.status_code, 400)

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        # define a dictionary to represent an unregistered user
        not_a_user = {
            'email': 'not_a_user@example.com',
            'password': 'nope'
        }
        # send a POST request to /auth/login with the data above
        res = self.client().post('/api/auth/login', data=not_a_user)
        # get the result in json
        result = json.loads(res.data.decode())

        # assert that this response must contain an error message
        # and an error status code 401(Unauthorized)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            result['message'], "Invalid credentials, Please try again.")
