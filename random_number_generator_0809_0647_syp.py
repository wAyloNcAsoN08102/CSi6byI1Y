# 代码生成时间: 2025-08-09 06:47:46
import asyncio
import random
from sanic import Sanic, response
def generate_random_number(min_value, max_value):
    """Generate a random number between min_value and max_value.
    Args:
        min_value (int): The minimum value of the random number.
        max_value (int): The maximum value of the random number.
    Returns:
        int: A random number between min_value and max_value.
    Raises:
        ValueError: If min_value is greater than max_value.
    """
    if min_value >= max_value:
        raise ValueError("min_value must be less than max_value")
    return random.randint(min_value, max_value)

app = Sanic("Random Number Generator")

@app.route("/random", methods=["GET"])
async def random_number(request):
    """Endpoint to generate a random number.
    Args:
        request (sanic.request.Request): The HTTP request object.
    Returns:
        response (sanic.response.json): A JSON response with a random number.
    """
    try:
        min_value = request.args.get("min", type=int, default=1)
        max_value = request.args.get("max", type=int, default=100)
        random_number = generate_random_number(min_value, max_value)
        return response.json({"random_number": random_number})
    except ValueError as e:
        return response.json({"error": str(e)}, status=400)
    except Exception as e:
        return response.json({"error": "Internal Server Error"}, status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)