# 代码生成时间: 2025-08-26 20:53:40
import sanic
from sanic.response import html, json
from jinja2 import Environment, FileSystemLoader
import plotly.graph_objects as go
import base64
import numpy as np

"""
Interactive Chart Generator using Sanic framework.
This module creates an interactive web server that generates charts based on user input.
"""

# Set up the Sanic app
app = sanic.Sanic('InteractiveChartGenerator')

# Set up the Jinja2 template environment
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('index.html')

# Define the route for the main page
@app.route('/')
async def main_page(request):
    """
    Returns the main page of the application.
    """
    return html(template.render())

# Define the route for generating charts
@app.route('/chart', methods=['POST'])
async def generate_chart(request):
    """
    Generates an interactive chart based on user input.
    Error handling is included to catch and respond to bad requests.
    """
    try:
        # Get the user input from the request
        x_data = request.json.get('x')
        y_data = request.json.get('y')

        # Check if the required data is present
        if x_data is None or y_data is None:
            return json({'error': 'Missing x or y data'}, status=400)

        # Generate the chart
        fig = go.Figure(data=[go.Scatter(x=x_data, y=y_data)])
        fig.update_layout(title='Interactive Chart', xaxis_title='X-axis', yaxis_title='Y-axis')

        # Encode the chart as a base64 string
        plotly_html = fig.to_html(full_html=False)
        plotly_html_base64 = base64.b64encode(plotly_html.encode()).decode()

        # Return the chart as a JSON response
        return json({'chart': plotly_html_base64}, status=200)
    except Exception as e:
        # Return a generic error response in case of an unexpected error
        return json({'error': 'An error occurred while generating the chart'}, status=500)

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

"""
To test the application, run the server and navigate to http://localhost:8000/ in your browser.
You can then post data to /chart with the required x and y data to generate an interactive chart.
"""