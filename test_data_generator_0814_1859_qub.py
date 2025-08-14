# 代码生成时间: 2025-08-14 18:59:46
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError
from faker import Faker

# 创建 Faker 实例，用于生成测试数据
fake = Faker()

app = Sanic('Test Data Generator')

@app.route('/test-data', methods=['GET'])
async def generate_test_data(request):
    """
    生成并返回测试数据的接口
    
    返回值：
        - JSON格式的测试数据
    """
    try:
        # 生成测试数据
        data = {
            'name': fake.name(),
            'email': fake.email(),
            'address': fake.address(),
            'phone_number': fake.phone_number()
        }
        # 返回生成的测试数据
        return response.json({'status': 'success', 'data': data})
    except Exception as e:
        # 错误处理
        raise ServerError('Failed to generate test data', status_code=500)

if __name__ == '__main__':
    # 启动 Sanic 应用
    app.run(host='0.0.0.0', port=8000, debug=True)
