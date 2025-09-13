# 代码生成时间: 2025-09-14 01:23:34
import unittest
from sanic import Sanic
from sanic.response import json
from sanic.testing import SanicTestClient
from your_module import app  # Replace 'your_module' with the name of your Sanic app module

# Define a test class inheriting from unittest.TestCase
class SanicAppTest(unittest.TestCase):

    def setUp(self):
        # Instantiate the Sanic app and create a test client
        self.app = app.create_test_client()

    def test_home_route(self):
        # Test the home route
        response = self.app.get('/')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'message': 'Hello World'})

    def test404_route(self):
        # Test a route that should return a 404
        response = self.app.get('/non_existent_route')
        self.assertEqual(response.status, 404)

    def test_error_handling(self):
        # Test that the error handling route returns the correct status code
        response = self.app.get('/error_handling_route')
        self.assertEqual(response.status, 500)

# Run the tests
if __name__ == '__main__':
    unittest.main(verbosity=2)