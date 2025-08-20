# 代码生成时间: 2025-08-21 05:05:21
import sanic
from sanic.response import json
from urllib.parse import urlparse
import validators

# 创建Sanic应用
app = sanic.Sanic("UrlValidatorService")

# 定义一个路由，用于验证URL链接的有效性
@app.route("/validate", methods=["POST"])
async def validate_url(request: sanic.Request):
    # 从请求体中获取URL
    url = request.json.get("url")

    # 检查URL是否提供了
    if url is None:
        return json({"error": "URL is required in the request body."}, status=400)

    # 使用validators模块来验证URL
    if validators.url(url):
        return json({"message": "URL is valid."})
    else:
        return json({"error": "Invalid URL."}, status=400)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
