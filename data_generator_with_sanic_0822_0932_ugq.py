# 代码生成时间: 2025-08-22 09:32:17
import random
from sanic import Sanic
from sanic.response import json

# 定义一个测试数据生成器函数
def generate_test_data():
    # 随机生成测试数据
    test_data = {
        'id': random.randint(1, 100),
        'name': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)),
        'age': random.randint(18, 60),
        'email': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)) + "@example.com"
    }
    return test_data

# 创建Sanic应用
app = Sanic("DataGeneratorApp")

# 定义一个用于生成测试数据的路由
@app.route("/generate", methods=["GET"])
async def generate(request):
    try:
        # 生成测试数据
        data = generate_test_data()
        # 返回生成的测试数据
        return json({"data": data})
    except Exception as e:
        # 处理生成测试数据时的错误
        return json({"error": str(e)})

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)