# 代码生成时间: 2025-09-20 18:50:51
import logging
from sanic import Sanic, response
from sanic.log import logger as sanic_logger
from sanic.exceptions import ServerError, ServerErrorMiddleware
import traceback
import os

# 设置日志配置
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# 定义错误日志收集器服务
app = Sanic('ErrorLoggerService')

# 错误处理中间件
class ErrorLoggerMiddleware(ServerErrorMiddleware):
    async def error_handler(self, request, exception):
        # 捕获和记录异常信息
        traceback_str = ''.join(traceback.format_exc())
        logger.error(f"Exception in {request.path}:
{traceback_str}")
        return response.json({'error': 'Internal Server Error'}, status=500)

# 路由处理
@app.route('/logs', methods=['GET'])
async def log_requests(request): 
    # 返回错误日志文件路径供前端下载
    log_file_path = os.path.join(os.getcwd(), 'logs', 'error.log')
    return response.file(log_file_path)

# 启动应用
if __name__ == '__main__':
# 优化算法效率
    app.run(host='0.0.0.0', port=8000, workers=1, debug=True)
# 扩展功能模块