# 代码生成时间: 2025-09-02 10:57:57
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.response import json

# 创建Sanic应用
app = Sanic("api_response_formatter")

class APIResponseFormatter:
    """API响应格式化工具。
    
    用于将API响应格式化为统一的格式。
    
    Attributes:
        ok (bool): 响应是否成功。
        data (dict): 响应数据。
        error (str): 错误信息。
    """
    def __init__(self, ok: bool, data: dict = None, error: str = None):
        self.ok = ok
        self.data = data if data is not None else {}
        self.error = error

    def to_dict(self) -> dict:
        """将响应格式化为字典。"""
        response_dict = {"ok": self.ok}
        if self.data:
            response_dict["data"] = self.data
        if self.error:
            response_dict["error"] = self.error
        return response_dict

    def to_json(self) -> str:
        """将响应格式化为JSON字符串。"""
        return json(self.to_dict())

@app.route("/format", methods=["GET", "POST"])
async def format_response(request: Sanic.Request):
    """
    格式化响应数据。
    
    接收请求参数，返回格式化后的响应数据。
    
    Args:
        request (Sanic.Request): 请求对象。
    
    Returns:
        response: 格式化后的响应数据。
    
    Raises:
        ServerError: 如果请求参数无效。
    """
    try:
        # 获取请求参数
        params = request.args if request.method == "GET" else request.json

        # 检查请求参数
        if not params:
            raise ServerError("请求参数无效")

        # 格式化响应数据
        ok = params.get("ok", True)
        data = params.get("data", {})
        error = params.get("error", None)

        response_formatter = APIResponseFormatter(ok, data, error)
        return response_formatter.to_json()
    
    except Exception as e:
        # 错误处理
        error_message = f"内部服务器错误: {str(e)}"
        return response.json({'ok': False, 'error': error_message}, status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
