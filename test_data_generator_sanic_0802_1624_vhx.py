# 代码生成时间: 2025-08-02 16:24:06
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError
from faker import Faker
from random import randint

# 初始化 Faker 生成器
fake = Faker()

app = Sanic("Test Data Generator")

# 定义生成测试数据的函数
def generate_test_data():
    """
    生成测试数据
    :return: 测试数据字典
    """
    try:
        # 使用 Faker 生成随机数据
        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "address": fake.address(),
            "phone_number": fake.phone_number(),
            "age": randint(18, 65)
        }
        return data
    except Exception as e:
        # 错误处理
        raise ServerError("Failed to generate test data", str(e))

# 定义 Sanic 路由和视图函数
@app.route("/generate", methods="GET")
async def generate(request):
    """
    生成并返回测试数据的视图函数
    :param request: Sanic 请求对象
    :return: 包含测试数据的 JSON 响应
    """
    try:
        data = generate_test_data()
        return response.json(data)
    except ServerError as e:
        # 错误处理
        return response.json({"error": str(e)}, status=500)

# 应用启动逻辑
if __name__ == "__main__":
    # 确保异步事件循环运行
    asyncio.ensure_future(app.run(host="0.0.0.0", port=8000, auto_reload=False))
    print("Server is running on http://0.0.0.0:8000")
