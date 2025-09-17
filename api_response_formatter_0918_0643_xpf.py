# 代码生成时间: 2025-09-18 06:43:59
import sanic
from sanic.response import json
from sanic.exceptions import ServerError, ClientError

"""
API Response Formatter is a tool designed to standardize and format API responses.
It provides a simple way to send consistent, structured responses back to clients."""

class ApiResponseFormatter:
    """
    A class to format API responses.
    """
    def __init__(self):
        pass

    def format_success(self, data, message="Success"):
        """
        Formats a successful API response.

        Args:
            data (dict): The data to be returned in the response.
            message (str): The success message. Defaults to 'Success'.

        Returns:
            dict: A formatted success response.
        """
        return {
            "status": "success",
            "message": message,
            "data": data
        }

    def format_error(self, code, message="Error occurred"):
        """
        Formats an error API response.

        Args:
            code (int): The error code.
            message (str): The error message. Defaults to 'Error occurred'.

        Returns:
            dict: A formatted error response.
        """
        return {
            "status": "error",
            "code": code,
            "message": message
        }

    def send_success_response(self, request, data, message="Success"):
        """
        Sends a formatted successful API response to the client.

        Args:
            request: The Sanic request object.
            data (dict): The data to be returned in the response.
            message (str): The success message. Defaults to 'Success'.
        """
        response = self.format_success(data, message)
        return json(response)

    def send_error_response(self, request, code, message="Error occurred"):
        """
        Sends a formatted error API response to the client.

        Args:
            request: The Sanic request object.
            code (int): The error code.
            message (str): The error message. Defaults to 'Error occurred'.
        """
        response = self.format_error(code, message)
        return json(response)

# Create a Sanic app
app = sanic.Sanic('api_response_formatter')

# Instantiate the ApiResponseFormatter class
response_formatter = ApiResponseFormatter()

@app.route('/')
async def test(request):
    try:
        # Simulate a successful response
        data = {"key": "value"}
        return response_formatter.send_success_response(request, data, "Test successful")
    except Exception as e:
        return response_formatter.send_error_response(request, 500, str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)