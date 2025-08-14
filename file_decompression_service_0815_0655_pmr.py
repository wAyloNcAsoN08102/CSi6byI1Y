# 代码生成时间: 2025-08-15 06:55:32
import zipfile
import sanic
from sanic.response import text, file as sanic_file
from sanic.exceptions import ServerError, NotFound, BadRequest
from sanic.handlers import ErrorHandler
from sanic import request
from sanic.log import logger
import os
import tempfile
import shutil

# 创建一个Sanic应用
app = sanic.Sanic('file_decompression_service')

# 错误处理器
class CustomErrorHandler(ErrorHandler):
    async def default(self, exception, context):
        return text('An error occurred: ' + str(exception), status=500)

# 定义解压文件的路由
@app.route('/decompress', methods=['POST'])
async def decompress_file(request):
    # 获取上传的文件
    file = request.files.get('file')
    if not file:
        raise BadRequest('No file provided')

    # 保存临时文件
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file.body)
        tmp_file_path = tmp_file.name

    try:
        # 解压文件
        with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
            zip_ref.extractall('extracted_files')
    except zipfile.BadZipFile:
        raise BadRequest('Invalid zip file')
    except Exception as e:
        raise ServerError(str(e))
    finally:
        # 删除临时文件
        os.remove(tmp_file_path)

    # 返回解压成功消息
    return text('File decompressed successfully.')

# 设置全局错误处理器
app.error_handler.add(ServerError, CustomErrorHandler())
app.error_handler.add(NotFound, CustomErrorHandler())
app.error_handler.add(BadRequest, CustomErrorHandler())

# 运行应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)