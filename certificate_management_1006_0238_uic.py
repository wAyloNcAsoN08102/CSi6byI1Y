# 代码生成时间: 2025-10-06 02:38:26
import os
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound, abort
from sanic.request import Request
from sanic.response import json

# 证书管理系统配置
CERTIFICATE_DIR = 'certificates/'
if not os.path.exists(CERTIFICATE_DIR):
    os.makedirs(CERTIFICATE_DIR)

# 初始化Sanic应用
app = Sanic("Certificate Management System")

# 证书信息存储结构
certificates = {}

# 获取证书列表
@app.route("/certificates", methods=["GET"])
async def get_certificates(request: Request):
    """
    返回所有证书信息的列表
    """
    return json(certificates)

# 添加证书
@app.route("/certificates", methods=["POST"])
async def add_certificate(request: Request):
    """
    添加一个新的证书到系统中
    """
    data = request.json
    if 'serial_number' not in data or 'name' not in data:
        abort(400, 'Invalid data format')
    certificates[data['serial_number']] = data
    return json({'message': 'Certificate added successfully'})

# 获取单个证书信息
@app.route("/certificates/<serial_number>", methods=["GET"])
async def get_certificate(request: Request, serial_number: str):
    """
    根据序列号返回单个证书信息
    """
    if serial_number in certificates:
        return json(certificates[serial_number])
    else:
        abort(404, 'Certificate not found')

# 更新证书信息
@app.route("/certificates/<serial_number>", methods=["PUT"])
async def update_certificate(request: Request, serial_number: str):
    """
    更新指定序列号的证书信息
    """
    data = request.json
    if serial_number in certificates:
        certificates[serial_number].update(data)
        return json({'message': 'Certificate updated successfully'})
    else:
        abort(404, 'Certificate not found')

# 删除证书
@app.route("/certificates/<serial_number>", methods=["DELETE"])
async def delete_certificate(request: Request, serial_number: str):
    """
    删除指定序列号的证书
    """
    if serial_number in certificates:
        del certificates[serial_number]
        return json({'message': 'Certificate deleted successfully'})
    else:
        abort(404, 'Certificate not found')

# 错误处理器
@app.exception(NotFound)
async def not_found_exception_handler(request, exception):
    return response.json({
        'message': 'The resource was not found.',
        'error': str(exception)
    }, status=404)

@app.exception(ServerError)
async def server_error_exception_handler(request, exception):
    return response.json({
        'message': 'Internal Server Error',
        'error': str(exception)
    }, status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)