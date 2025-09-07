# 代码生成时间: 2025-09-08 02:44:23
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import ServerError, Unauthorized, Forbidden
from sanic_openapi import doc, swagger_blueprint
from sanic_jwt_extended import JWTManager, jwt_required, get_jwt, create_access_token
from datetime import timedelta

# 定义JWT密钥和过期时间
SECRET_KEY = 'your-secret-key'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = Sanic('UserAuthService')
jwt = JWTManager(app)

# 用户身份验证装饰器
@jwt_required()
def get_user(request, *args, **kwargs):
    return request.user  # 返回当前用户信息

# 用户注册端点
@app.route('/register', methods=['POST'])
@doc.body({
    'username': 'string',
    'password': 'string',
},
    examples=[
        {'username': 'JohnDoe', 'password': 'password123'}
    ])
async def register_user(request):
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return json({'error': 'Missing username or password'}, status=400)
    # 这里应该添加注册逻辑，例如保存用户信息到数据库
    # 假设注册成功
    return json({'message': 'User registered successfully'}, status=201)

# 用户登录端点
@app.route('/login', methods=['POST'])
@doc.body({
    'username': 'string',
    'password': 'string',
},
    examples=[
        {'username': 'JohnDoe', 'password': 'password123'}
    ])
async def login_user(request):
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return json({'error': 'Missing username or password'}, status=400)
    # 这里应该添加登录逻辑，例如验证用户信息和密码
    # 假设登录成功
    # 创建访问令牌
    access_token = create_access_token(identity=username,
                                    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return json({'access_token': access_token}, status=200)

# 用户信息端点
@app.route('/profile', methods=['GET'])
@doc.summary('Get user profile')
@jwt_required()
async def profile(request):
    current_user = get_user(request)
    return json({'username': current_user.username}, status=200)

# 添加Swagger文档
app.blueprint(swagger_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
