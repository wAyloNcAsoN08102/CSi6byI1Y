# 代码生成时间: 2025-10-10 22:11:46
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError, ServerErrorMiddleware
from sanic.request import Request
from sanic.response import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Sanic('RPCServer')

# RPC服务字典
rpc_services = {}

# 注册RPC服务
def register_rpc_service(name, service_func):
    rpc_services[name] = service_func
    logger.info(f"Registered RPC service: {name}")

# RPC服务中间件
@app.middleware('request')
async def rpc_service_middleware(request: Request):
    request.ctx.rpc_service_name = None
    request.ctx.rpc_service_func = None
    if 'rpc_service' in request.args:
        service_name = request.args.get('rpc_service')
        if service_name in rpc_services:
            request.ctx.rpc_service_name = service_name
            request.ctx.rpc_service_func = rpc_services[service_name]
        else:
            raise ServerError('RPC service not found', status_code=404)

# RPC服务处理
@app.route('/api/rpc', methods=['POST'])
async def rpc_service(request: Request):
    try:
        if not request.ctx.rpc_service_name or not request.ctx.rpc_service_func:
            raise ServerError('No RPC service specified', status_code=400)

        # 从请求中提取参数
        data = request.json
        params = data.get('params', [])

        # 调用RPC服务
        result = await asyncio.to_thread(request.ctx.rpc_service_func, *params)

        # 返回结果
        return response.json({'result': result})
    except Exception as e:
        logger.error(f'RPC service error: {e}')
        raise ServerError('RPC service error', status_code=500)

# 错误处理中间件
@app.exception(ServerError)
async def handle_server_error(request: Request, exception: ServerError):
    logger.error(exception)
    return response.json({'error': str(exception)})

# RPC服务示例
def example_service(param1, param2):
    # 模拟一个简单的计算
    result = param1 + param2
    logger.info(f'Executed example_service with params: {param1}, {param2}')
    return result

# 注册示例RPC服务
register_rpc_service('example', example_service)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, auto_reload=False)
