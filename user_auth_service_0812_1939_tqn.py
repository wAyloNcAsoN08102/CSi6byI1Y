# 代码生成时间: 2025-08-12 19:39:38
import json
from sanic import Sanic, request, response
from sanic.exceptions import ServerError
from sanic_jwt import Initialize, JWTManager
from sanic_jwt.decorators import protected, scoped
from sanic_jwt.exceptions import AuthenticationFailed, FreshTokenRequired

# 初始化Sanic应用
app = Sanic("UserAuthService")

# 配置JWT认证
app.config.FROM_ENV = True
jwt = JWTManager(app)

# 假设的用户数据库（实际应用中应替换为数据库操作）
user_db = {
    "username": "user",
    "password": "password"
}

# 用户认证路由
@app.route("/login", methods=["POST"])
async def login(request):
    # 获取请求体中的用户名和密码
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username is None or password is None:
        return response.json(
            {
                "error": "Missing username or password"
            },
            status=400
        )
    
    # 验证用户名和密码
    if username != user_db["username"] or password != user_db["password"]:
        raise AuthenticationFailed("Invalid credentials", status_code=401)
    
    # 创建一个JWT token
    token = jwt.encode({"user_id": username}, app.config["SECRET_KEY"])
    return response.json(
        {
            "token": token,
            "fresh_token": jwt.encode({"user_id": username}, app.config["SECRET_KEY"], fresh=True)
        },
        status=200
    )

# 受保护的路由
@protected()
@app.route("/protected")
async def protected_route(request):
    # 如果用户未认证，则抛出异常
    if not request.ctx.user:
        raise FreshTokenRequired("User is not authenticated", status_code=401)
    
    # 返回受保护的数据
    return response.json(
        {
            "message": "You have accessed a protected route"
        },
        status=200
    )

# 启动Sanic应用
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
