# 代码生成时间: 2025-08-13 03:50:05
import logging
from sanic import Sanic, response
from sanic.exceptions import ServerError, ServerErrorMiddleware
from sanic.request import Request
from sanic.response import json
from datetime import datetime
import os

# 设置日志文件路径
LOG_FILE_PATH = "error_log.txt"

# 创建Sanic应用
app = Sanic("ErrorLogCollector")

# 配置日志
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# 错误处理中间件
@app.exception(ServerError)
async def handle_server_error(request: Request, exception: ServerError):
    # 记录错误日志
    logging.error(f"{exception.__repr__()}")
    return json({"error": "Internal Server Error"}, status=500)

# 定义一个路由来触发一个错误
@app.route("/error")
async def trigger_error(request: Request):
    # 故意引发一个除以零的错误
    result = 1 / 0
    return response.json({"result": result})

# 定义一个路由来查看错误日志
@app.route("/logs")
async def view_logs(request: Request):
    try:
        with open(LOG_FILE_PATH, 'r') as f:
            log_content = f.read()
        return response.json({"logs": log_content})
    except FileNotFoundError:
        return response.json({"error": "Log file not found"}, status=404)

# 确保日志文件存在
if not os.path.exists(LOG_FILE_PATH):
    with open(LOG_FILE_PATH, 'w') as f:
        f.write('')

# 运行应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)