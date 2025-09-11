# 代码生成时间: 2025-09-11 17:20:23
import psutil
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json

# Initialize the Sanic app
def create_app():
    app = Sanic('system_monitor')

    @app.route('/cpu', methods=['GET'])
    async def cpu_usage(request: Request):
        """
        Endpoint to get CPU usage percentage.

        :return: CPU usage percentage as a JSON response.
        """
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            return json({'cpu_usage': cpu_usage})
        except Exception as e:
            return response.text(f'Error: {e}', status=500)

    @app.route('/memory', methods=['GET'])
    async def memory_usage(request: Request):
        """
        Endpoint to get memory usage information.

        :return: Memory usage information as a JSON response.
        """
        try:
            memory = psutil.virtual_memory()
            return json({'memory_usage': memory.percent, 'memory_total': memory.total})
        except Exception as e:
            return response.text(f'Error: {e}', status=500)

    @app.route('/disk', methods=['GET'])
    async def disk_usage(request: Request):
        """
        Endpoint to get disk usage information.

        :return: Disk usage information as a JSON response.
        """
        try:
            disk = psutil.disk_usage('/')
            return json({'disk_usage': disk.percent, 'disk_total': disk.total})
        except Exception as e:
            return response.text(f'Error: {e}', status=500)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000)