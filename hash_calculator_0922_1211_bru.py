# 代码生成时间: 2025-09-22 12:11:10
import hashlib
def create_hash(input_string, algorithm='sha256', encoding='utf-8', return_digest=True):
    """
    创建哈希值的函数

    参数：
    input_string (str): 待哈希的字符串
    algorithm (str): 哈希算法，默认为 'sha256'
    encoding (str): 字符串编码，默认为 'utf-8'
    return_digest (bool): 是否返回哈希摘要，默认为 True

    返回：
    str: 哈希值的十六进制字符串或者哈希摘要
    """
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(input_string.encode(encoding))
    if return_digest:
        return hash_obj.digest()
    else:
        return hash_obj.hexdigest()

def calculate_hash(request, input_string):
    """
    计算哈希值的视图函数

    参数：
    request (sanic.Request): 请求对象
    input_string (str): 待哈希的字符串
    """
    try:
        algorithm = request.args.get('algorithm', 'sha256')
        encoding = request.args.get('encoding', 'utf-8')
        return_digest = request.args.get('return_digest', True)
        hash_value = create_hash(input_string, algorithm, encoding, 
                                return_digest == 'True')
        return json({'success': True, 'hash': hash_value})
    except Exception as e:
        return json({'success': False, 'error': str(e)})

def create_app():
    """
    创建 Sanic 应用程序
    """
    app = Sanic(__name__)
    @app.route("/hash", methods=["GET"])
    async def hash_handler(request):
        return calculate_hash(request, request.args.get('input'))
    return app
def main():
    """
    应用程序的入口点
    """
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)
def __sanic_start_heartbeat__():
    """
    Sanic 应用程序的心跳函数，用于启动应用程序
    """
    main()
if __name__ == '__main__':
    __sanic_start_heartbeat__()
