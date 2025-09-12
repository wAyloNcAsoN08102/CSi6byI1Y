# 代码生成时间: 2025-09-13 01:54:39
import math
import sanic
from sanic.response import json
from sanic.exceptions import ServerError, ClientError

# 定义一个随机数生成器的Sanic视图功能
app = sanic.Sanic('RandomNumberGeneratorApp')

@app.route('/random', methods=['GET'])
async def generate_random(request):
    # 从查询参数中获取最小值和最大值
    min_value = request.args.get('min', type=int, default=0)
    max_value = request.args.get('max', type=int, default=100)

    # 验证参数有效性
    if min_value > max_value:
        raise ClientError("Bad Request", status_code=400, description="Minimum value cannot be greater than maximum value.")

    try:
        # 生成随机数
        random_value = math.floor(math.random() * (max_value - min_value + 1)) + min_value
        return json({'random_number': random_value})
    except Exception as e:
        # 捕捉并处理任何异常
        raise ServerError('Internal Server Error', status_code=500, description=str(e))

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
