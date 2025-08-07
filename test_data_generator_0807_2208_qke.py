# 代码生成时间: 2025-08-07 22:08:22
import json
from sanic import Sanic, response
from sanic.response import json as json_response
from faker import Faker

# 定义一个Sanic应用
app = Sanic("Test Data Generator")

# 创建一个Faker实例用于生成测试数据
fake = Faker()

# 定义一个路由，用于生成测试数据
@app.route("/generate", methods=["GET"])
async def generate_test_data(request):
    # 检查请求参数
    if "count" not in request.args:
        return json_response(
            {
                "error": "Missing required parameter: count"
            },
            status=400
        )

    # 尝试从请求参数中获取数据数量
    try:
        count = int(request.args.get("count", 1))
    except ValueError:
        return json_response(
            {
                "error": "Invalid value for count parameter"
            },
            status=400
        )

    # 生成测试数据
    test_data = [
        {
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip_code": fake.zipcode(),
            "country": fake.country(),
        } for _ in range(count)
    ]

    # 返回生成的测试数据
    return response.json(test_data)

# 定义一个路由，用于返回应用信息
@app.route("/info", methods=[