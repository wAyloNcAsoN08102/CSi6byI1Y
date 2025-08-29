# 代码生成时间: 2025-08-30 01:43:57
import json
from sanic import Sanic, response
from sanic.response import json as sanic_json
from sanic.exceptions import ServerError
from sanic_jwt import 
    JWTManager,
    exceptions,
    Initialize

# 初始化Sanic应用
app = Sanic('UserAuthService')

# 配置JWT
app.config['JWT_ENABLE'] = True
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['AUTH_HEADER_TYPE'] = 'Bearer'
jwt = JWTManager(app)

# 假定的用户数据库
users_db = {
    "user1": {"username": "user1", "password": "pass1"},
    "user2": {"username": "user2", "password": "pass2"}
}

# 错误处理
@app.exception(exceptions.NoAuthorizationError)
async def auth_error(request, exception):
    return sanic_json({'message': 'Authorization error'}, status=401)

@app.exception(exceptions.ExpiredSignatureError)
async def expired_error(request, exception):
    return sanic_json({'message': 'Expired token'}, status=401)

# 用户登录接口
@app.route('/login', methods=['POST'])
async def login(request):
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username not in users_db or users_db[username]['password'] != password:
        return response.json({'message': 'Invalid credentials'}, status=401)
    # 创建token
    token = jwt.create_token(identity=username)
    return response.json({'message': 'Login successful', 'token': token})

# 用户身份验证接口
@app.route('/verify', methods=['POST'])
@jwt.requires_auth
async def verify(request):
    # 获取当前用户身份
    user_identity = request.ctx.auth.get('identity')
    return response.json({'message': 'User verified', 'user': user_identity})

# 启动Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
