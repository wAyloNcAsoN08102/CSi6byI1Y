# 代码生成时间: 2025-08-01 20:05:49
import sanic
from sanic.response import json
from sanic.exceptions import ServerError
import hashlib

# 定义哈希计算服务
class HashCalculatorService:
    def __init__(self):
        pass

    # 计算哈希值
    def calculate_hash(self, data, algorithm='sha256'):
        try:
            hash_func = getattr(hashlib, algorithm)()
            hash_func.update(data.encode('utf-8'))
            return hash_func.hexdigest()
        except Exception as e:
            raise ServerError(f"Failed to calculate hash: {e}")

# 定义Sanic应用
app = sanic.Sanic("HashCalculator")
hash_service = HashCalculatorService()

# 定义路由
@app.route("/", methods=["GET"])
async def index(request):
    return json({"message": "Welcome to Hash Calculator Service"})

@app.route("/calculate", methods=["POST"])
async def calculate_hash(request):
    # 获取请求体中的参数
    data = request.json.get("data")
    algorithm = request.json.get("algorithm", "sha256")

    # 校验参数
    if not data:
        raise ServerError("Missing 'data' in request")

    # 调用服务计算哈希值
    try:
        hash_value = hash_service.calculate_hash(data, algorithm)
        return json({"hash": hash_value})
    except ServerError as e:
        return json({"error": str(e)}, status=500)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)