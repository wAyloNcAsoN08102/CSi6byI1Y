# 代码生成时间: 2025-09-19 15:09:34
import psutil
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.log import logger

# 初始化Sanic应用
app = Sanic('SystemPerformanceMonitor')

# 定义异常处理
@app.exception
async def handle_request_exception(request, exception):
    if isinstance(exception, ServerError):
        logger.error(f"ServerError: {exception}")
        return response.json({'error': str(exception)}, status=500)
    else:
        logger.error(f"Exception: {exception}")
        return response.json({'error': 'Internal Server Error'}, status=500)

# 获取CPU使用率的API
@app.route('/api/cp_usage')
async def cpu_usage(request):
    try:
        # 获取CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        return response.json({'cpu_usage': cpu_percent})
    except Exception as e:
        logger.error(f"Failed to get CPU usage: {e}")
        return response.json({'error': 'Failed to get CPU usage'}, status=500)

# 获取内存使用情况的API
@app.route('/api/mem_usage')
async def mem_usage(request):
    try:
        # 获取内存使用情况
        mem = psutil.virtual_memory()
        return response.json({
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'percentage': mem.percent
        })
    except Exception as e:
        logger.error(f"Failed to get memory usage: {e}")
        return response.json({'error': 'Failed to get memory usage'}, status=500)

# 获取磁盘使用情况的API
@app.route('/api/disk_usage')
async def disk_usage(request):
    try:
        # 获取磁盘使用情况
        partitions = psutil.disk_partitions()
        disk_usage = {}
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_usage[partition.device] = {
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percentage': usage.percent
            }
        return response.json(disk_usage)
    except Exception as e:
        logger.error(f"Failed to get disk usage: {e}")
        return response.json({'error': 'Failed to get disk usage'}, status=500)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, auto_reload=True)