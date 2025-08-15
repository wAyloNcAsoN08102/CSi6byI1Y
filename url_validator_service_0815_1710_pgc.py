# 代码生成时间: 2025-08-15 17:10:09
from sanic import Sanic, response
from sanic.exceptions import ServerError
from urllib.parse import urlparse
import requests

# 初始化Sanic应用程序
app = Sanic("URL Validator Service")

# 定义一个函数来验证URL是否有效
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

# 定义一个异步函数来检查URL是否可访问
async def check_url_accessibility(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        return False

# 定义一个路由来处理URL验证请求
@app.route("/validate", methods=["GET"])
async def validate_url(request):
    url_to_check = request.args.get("url")
    if url_to_check:
        is_valid = is_valid_url(url_to_check)
        is_accessible = await check_url_accessibility(url_to_check)

        if is_valid and is_accessible:
            return response.json({
                "valid": True,
                "message": "The URL is valid and accessible."
            })
        elif is_valid and not is_accessible:
            return response.json({
                "valid": True,
                "message": "The URL is valid but not accessible."
            })
        else:
            return response.json({
                "valid": False,
                "message": "The URL is not valid."
            })
    else:
        raise ServerError("URL parameter is missing.", status_code=400)

# 运行Sanic应用程序
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)