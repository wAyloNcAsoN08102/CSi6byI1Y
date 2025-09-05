# 代码生成时间: 2025-09-05 14:04:08
import random
from sanic import Sanic, response

# 创建随机数生成器应用
app = Sanic('random_number_generator')

"""随机数生成器蓝图"""
@app.route('/random/<int:max>', methods=['GET'])
async def generate_random_number(request, max):
    """
    根据请求参数生成一个随机数，并返回给客户端。
    :param request: 请求对象
    :param max: 最大值（整数）
    :return: JSON格式的响应，包含随机数
    """
    try:
        # 生成随机数
        random_number = random.randint(0, max)
        return response.json({'random_number': random_number})
    except Exception as e:
        # 错误处理
        return response.json({'error': str(e)}, status=500)

if __name__ == '__main__':
    # 运行应用
    app.run(host='0.0.0.0', port=8000)