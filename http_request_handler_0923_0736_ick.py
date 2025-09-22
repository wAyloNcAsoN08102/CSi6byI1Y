# 代码生成时间: 2025-09-23 07:36:49
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound
from sanic.response import json as sanic_json

# 创建Sanic应用
app = Sanic(__name__)

# 定义全局数据字典
data = {"key": "value"}

# 定义HTTP请求处理函数
@app.route('/api/data', methods=['GET'])
def handle_get_request(request):
    """
    处理GET请求，返回全局数据字典的JSON表示。
    :param request: Sanic请求对象
    :return: JSON响应
    """
    try:
        return sanic_json(data)
    except Exception as e:
        raise ServerError(f"Error handling GET request: {e}")

# 定义POST请求处理函数
@app.route('/api/data', methods=['POST'])
def handle_post_request(request):
    """
    处理POST请求，更新全局数据字典。
    :param request: Sanic请求对象
    :return: JSON响应
    """
    try:
        # 解析请求体中的JSON数据
        data_update = request.json
        # 更新全局数据字典
        data.update(data_update)
        return sanic_json(data)
    except Exception as e:
        raise ServerError(f"Error handling POST request: {e}")

# 定义错误处理器
@app.exception(NotFound)
def handle_not_found(request, exception):
    """
    处理404错误。
    :param request: Sanic请求对象
    :param exception: 异常对象
    :return: JSON响应
    """
    return sanic_json({'error': 'Not found'}, status=404)

# 定义服务器错误处理器
@app.exception(ServerError)
def handle_server_error(request, exception):
    """
    处理服务器错误。
    :param request: Sanic请求对象
    :param exception: 异常对象
    :return: JSON响应
    """
    return sanic_json({'error': 'Internal server error'}, status=500)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)