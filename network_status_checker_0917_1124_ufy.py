# 代码生成时间: 2025-09-17 11:24:04
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError, ServerNotRunning
from sanic.request import Request
from urllib3 import PoolManager, ProxySchemeUnknown
from urllib3.exceptions import ProxySchemeUnknown as ProxyError

# 网络连接状态检查器
app = Sanic("NetworkStatusChecker")

# 检查网络连接状态的异步函数
async def check_connection(url):
    try:
        # 使用urllib3建立HTTP连接
        http = PoolManager()
        response = http.request("GET", url, timeout=5)
        return response.status
    except (ConnectionError, TimeoutError):
        # 网络连接异常
        return 503
    except ProxyError:
        # 代理设置错误
# 增强安全性
        return 502
    except Exception as e:
        # 其他异常
        print(f"An unexpected error occurred: {e}")
        return 500

# Sanic路由处理函数
@app.route("/check", methods=["GET"])
async def check_status(request: Request):
    # 从请求中获取URL
    url = request.args.get("url")
    if not url:
        return response.json({"error": "URL parameter is required"}, status=400)
    
    # 检查网络连接状态
    status_code = await check_connection(url)
    return response.json({"status": status_code})

# 异常处理
# 添加错误处理
@app.exception(ServerError)
async def handle_server_error(request, exception):
# 增强安全性
    return response.json({"error": "Internal Server Error"}, status=500)

@app.exception(ServerNotRunning)
async def handle_server_not_running(request, exception):
    return response.json({"error": "Server is not running"}, status=503)

# 主函数，用于启动Sanic服务
if __name__ == "__main__":
    # 启动Sanic服务器
    app.run(host="0.0.0.0", port=8000)