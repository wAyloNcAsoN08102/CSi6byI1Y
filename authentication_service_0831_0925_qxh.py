# 代码生成时间: 2025-08-31 09:25:54
from sanic import Sanic, response
from sanic.response import json
from sanic.exceptions import ServerError, Unauthorized
from sanic_jwt import Initialize, JWTManager

# Initialize the Sanic app
app = Sanic("AuthenticationService")

# Initialize the JWTManager
# You should replace SECRET_KEY with your own secret key
jwt = JWTManager(app, secret_key="YOUR_SECRET_KEY")

# Define user data for simplicity; in real applications, this should come from a database
users = {
    "user1": {"username": "user1", "password": "password1"},
    "user2": {"username": "user2", "password": "password2"}
}

# Endpoint for user authentication
@app.route("/login", methods=["POST"])
async def login(request):
    # Extract credentials from the request
    username = request.json.get("username")
    password = request.json.get("password")

    # Check if credentials are present
    if not username or not password:
        return json({"message": "Missing credentials"}, status=400)

    # Authenticate user
    user = users.get(username)
    if user and user["password"] == password:
        # Create JWT token
        token = jwt.create_token(identity=username)
        return json({"token": token}, status=200)
    else:
        # If authentication fails
        raise Unauthorized(
            "Invalid credentials",
            status_code=401
        )

# Error handler for unauthorized access
@app.exception(Unauthorized)
async def unauthorized(request, exception):
    return response.json(
        {
            "error": exception.args[0],
            "status": 401
        },
        status=exception.status_code
    )

# Error handler for internal server errors
@app.exception(ServerError)
async def server_error(request, exception):
    return response.json(
        {
            "error": "Internal Server Error",
            "status": 500
        },
        status=500
    )

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)