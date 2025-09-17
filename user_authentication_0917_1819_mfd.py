# 代码生成时间: 2025-09-17 18:19:33
import json
from sanic import Sanic, response
from sanic.response import json as sanic_json
from sanic.exceptions import ServerError, Unauthorized, NotFound
from sanic.request import Request
from sanic.handlers import ErrorHandler

# 假设用户数据存储
USER_DATA = {
    "user1": {"username": "user1", "password": "password1"},
    "user2": {"username": "user2", "password": "password2"},
}

class AuthError(ServerError):
    pass

def authenticate_user(request: Request):
    # 从请求中获取用户名和密码
    username = request.json.get("username")
    password = request.json.get("password")

    # 验证用户名和密码
    if not username or not password:
        raise AuthError(
            "Username and password are required.", status_code=401
        )
    user = USER_DATA.get(username)
    if not user or user["password"] != password:
        raise AuthError("Invalid username or password.", status_code=401)
    return user

app = Sanic("UserAuthenticationApp")

# 错误处理器
@app.exception(AuthError)
async def handle_auth_error(request, exception):
    return response.json({"error": exception.args[0]}, status=exception.status_code)

@app.post("/login")
async def login(request: Request):
    try:
        user = authenticate_user(request)
        return sanic_json({"message": "Login successful", "user": user})
    except AuthError as e:
        return response.json({"error": str(e)}, status=401)

if __name__ == "__main__":
    ErrorHandler(app)
    app.run(host="0.0.0.0", port=8000, debug=True)