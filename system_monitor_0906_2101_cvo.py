# 代码生成时间: 2025-09-06 21:01:01
import asyncio
import psutil
from sanic import Sanic, response


# 创建一个Sanic应用
app = Sanic("SystemMonitor")


# 系统性能监控API的路由
@app.route("/monitor/<interval:int>", methods=["GET"])
async def monitor(request, interval):
    """
    监控系统性能并返回结果
    :param request: HTTP请求
    :param interval: 监控间隔时间（秒）
    :return: JSON格式的系统性能数据
    """
    try:
        # 获取系统性能数据
        system_data = await get_system_data(interval)
        return response.json(system_data)
    except Exception as e:
        # 错误处理
        return response.json({"error": str(e)})


# 异步获取系统性能数据
async def get_system_data(interval):
    """
    异步获取系统性能数据
    :param interval: 监控间隔时间（秒）
    :return: 系统性能数据
    """
    system_data = {"cpu": {}, "memory": {}, "disk": {}, "network": {}}
    # 获取CPU使用率
    system_data["cpu"]["usage"] = psutil.cpu_percent(interval=interval)
    # 获取内存使用情况
    memory = psutil.virtual_memory()
    system_data["memory"]["total"] = memory.total
    system_data["memory"]["available"] = memory.available
    system_data["memory"]["used"] = memory.used
    system_data["memory"]["percent"] = memory.percent
    # 获取磁盘使用情况
    disk = psutil.disk_usage('/')
    system_data["disk"]["total"] = disk.total
    system_data["disk"]["used"] = disk.used
    system_data["disk"]["free"] = disk.free
    system_data["disk"]["percent"] = disk.percent
    # 获取网络使用情况
    net_io = psutil.net_io_counters()
    system_data["network"]["bytes_sent"] = net_io.bytes_sent
    system_data["network"]["bytes_recv"] = net_io.bytes_recv
    system_data["network"]["packets_sent"] = net_io.packets_sent
    system_data["network"]["packets_recv"] = net_io.packets_recv
    return system_data


# 运行Sanic应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)