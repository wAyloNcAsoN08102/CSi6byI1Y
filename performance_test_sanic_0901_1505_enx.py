# 代码生成时间: 2025-09-01 15:05:31
import asyncio
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.testing import sanic_test
from sanic.exceptions import ServerError
import json
import time
import requests
import asyncio

"""
Performance Test Script using Sanic framework
This script sets up a simple Sanic application and runs performance tests using the requests library.
"""

# Initialize the Sanic application
app = Sanic('PerformanceTestApp')

# Define a test route for performance testing
@app.route('/test', methods=['GET'])
async def test(request: Request):
    # Simulate some processing time
    time.sleep(0.1)
    return response.json({'message': 'Hello, World!'})

# Run the Sanic application
if __name__ == '__main__':
    # Start the server
    app.run(host='0.0.0.0', port=8000, auto_reload=False)


# Performance test function
async def performance_test():
    # Define the URL to test
    url = 'http://127.0.0.1:8000/test'

    # Start measuring time
    start_time = time.time()

    # Define the number of test requests
    num_requests = 100

    # Loop through each request
    for _ in range(num_requests):
        try:
            # Send a GET request to the test route
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                print(f'Request successful: {response.json()}')
            else:
                print(f'Request failed with status code: {response.status_code}')
        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the request
            print(f'Request failed with error: {e}')

    # Calculate the total time taken for all requests
    total_time = time.time() - start_time

    # Print the total time taken and the number of requests
    print(f'Total time taken: {total_time} seconds for {num_requests} requests')

    # Calculate the average response time per request
    avg_response_time = total_time / num_requests

    # Print the average response time per request
    print(f'Average response time: {avg_response_time} seconds per request')


# Run the performance test in an asyncio event loop
if __name__ == '__main__':
    asyncio.run(performance_test())