# 代码生成时间: 2025-08-18 10:08:13
import asyncio
from sanic import Sanic, text, response
from sanic.response import json
from sanic.exceptions import ServerError
from sanic_jwt_extended import JWTManager, jwt_required, get_jwt, create_access_token
from sanic_jwt_extended.exceptions import JWTException
from sanic_jwt_extended.utils import get_identity

# Initialize JWT manager
jwt = JWTManager(secret_key="your-secret-key")

app = Sanic("UserAuthService")

# Mock database for demonstration purposes
USERS_DATABASE = {
    "admin": "password123",
    "user": "password456"
}

# Endpoint to handle user login
@app.route("/login", methods=["POST"])
async def login(request):
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    # Check if provided credentials are correct
    if username in USERS_DATABASE and USERS_DATABASE[username] == password:
        access_token = create_access_token(identity=username)
        return response.json({
            "message": "Login successful",
            "access_token": access_token
        })
    else:
        raise ServerError("Invalid credentials", status_code=401)

# Endpoint to check user authentication
@app.route("/protected", methods=["GET"])
@jwt_required
async def protected(request):
    identity = get_identity(request)
    return response.json({
        "message": f"Welcome {identity}! This is a protected route."
    })

# Error handler for JWT exceptions
@app.exception(JWTException)
async def jwt_exception_handler(request, exception):
    return response.json({
        "message": str(exception),
        "success": False
    }, status=401)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, auto_reload=False)
