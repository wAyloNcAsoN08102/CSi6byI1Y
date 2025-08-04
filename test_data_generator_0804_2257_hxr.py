# 代码生成时间: 2025-08-04 22:57:57
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError, SanicException
from uuid import uuid4
from random import choice, randint
from faker import Faker

# 初始化 Faker 生成器
fake = Faker()

# 初始化 Sanic 应用
app = Sanic('Test Data Generator')

# 测试数据模板
data_template = {
    "id": "{}",
    "name": "name",
    "email": "email",
    "age": 0,
    "address": "address"
}

@app.route('/test_data/<int:num>', methods=['GET'])
async def generate_test_data(request, num: int):
    # 检查请求参数是否有效
    if num <= 0:
        return response.json({
            "error": "Invalid number of entries"
        }, status=400)
    
    # 生成测试数据
    test_data = []
    for _ in range(num):
        single_data = {
            "id": str(uuid4()),
            "name": fake.name(),
            "email": fake.email(),
            "age": randint(18, 99),
            "address": fake.address()
        }
        test_data.append(single_data)
    
    # 返回生成的测试数据
    return response.json(test_data)

# 错误处理器
@app.exception(ServerError)
async def handle_server_error(request, exception):
    # 记录错误日志
    print(f"An error occurred: {exception}")
    # 返回错误信息
    return response.json({
        "error": "Internal Server Error"
    }, status=500)

if __name__ == '__main__':
    # 运行 Sanic 应用
    app.run(host='0.0.0.0', port=8000, debug=True)