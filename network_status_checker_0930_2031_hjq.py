# 代码生成时间: 2025-09-30 20:31:35
import aiohttp
from sanic import Sanic
from sanic.response import json, text
from sanic.exceptions import ServerError
import asyncio
import socket

# 定义一个异步函数，用于检查网络连接状态
async def check_connection(host, port):
    try:
        # 使用aiohttp创建一个会话
        async with aiohttp.ClientSession() as session:
            # 尝试连接到指定的主机和端口
            async with session.get(f"http://{host}:{port}"):
                return True
    except aiohttp.ClientError:
        # 如果连接失败，返回False
        return False

# 创建一个Sanic应用
app = Sanic("NetworkStatusChecker")

# 定义一个路由，用于检查网络连接状态
@app.route("/check", methods=["GET"])
async def check_status(request):
    host = request.args.get("host")
    port = request.args.get("port", type=int)

    # 参数校验
    if not host or not port:
        return json({"error": "Missing required parameters"}, status=400)

    try:
        # 调用异步函数检查网络连接状态
        result = await check_connection(host, port)
        # 返回检查结果
        return json({"status": "connected" if result else "disconnected"}, status=200)
    except Exception as e:
        # 捕捉异常并返回错误信息
        return json({"error": str(e)}, status=500)

# 运行Sanic应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, auto_reload=False)