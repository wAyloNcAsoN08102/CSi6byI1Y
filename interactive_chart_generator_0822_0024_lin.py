# 代码生成时间: 2025-08-22 00:24:49
import sanic
from sanic.response import json, html
from sanic.exceptions import ServerError, abort
import numpy as np
import plotly.express as px


# Define the Interactive Chart Generator application
app = sanic.Sanic("Interactive Chart Generator")


# Generate a sample interactive chart
@app.route("/generate_chart", methods=["GET"])
async def generate_chart(request: sanic.Request):
    # Check for query parameters
    x = request.args.get("x")
    y = request.args.get("y")
    if not x or not y:
        abort(400, "Missing required query parameters 'x' and 'y'")

    # Generate a sample dataset
    data = {
        "x": np.array(eval(x)),
        "y": np.array(eval(y))
    }

    # Create a line chart
    chart = px.line(data, x="x", y="y")
    chart.update_layout(title="Interactive Line Chart")

    # Return the chart as HTML
    return html(chart.to_html())


# Error handler for 400 errors
@app.exception(ServerError)
async def server_error(request, exception):
    return json({"error": str(exception)}, status=400)


# Error handler for 404 errors
@app.exception(sanic.exceptions.NotFound)
async def not_found(request, exception):
    return json({"error": "Not Found"}, status=404)


# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
