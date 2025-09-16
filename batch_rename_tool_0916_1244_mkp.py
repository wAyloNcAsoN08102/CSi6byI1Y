# 代码生成时间: 2025-09-16 12:44:27
import os
from sanic import Sanic, response
from sanic.request import Request
from sanic.exceptions import ServerError, NotFound, abort
import re

"""
批量文件重命名工具
使用SANIC框架实现一个简单的REST API，用于批量重命名文件。
"""

app = Sanic("BatchRenameTool")

# 正则表达式用于验证文件名格式
FILE_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_\-\.]+$')

def rename_files(directory, rename_rules):
    """
    根据给定的重命名规则批量重命名文件
    :param directory: 文件所在的目录
    :param rename_rules: 重命名规则字典，key为原始文件名，value为新文件名
    :return: 重命名结果字典
    """
    results = {}
    for old_name, new_name in rename_rules.items():
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)
        if os.path.exists(old_path) and FILE_NAME_PATTERN.match(new_name):
            try:
                os.rename(old_path, new_path)
                results[old_name] = new_name
            except OSError as e:
                results[old_name] = str(e)
        else:
            results[old_name] = "File not found or invalid new name"
    return results

@app.route('(rename', methods=['POST'])
async def rename_handler(request: Request):
    """
    API端点处理文件批量重命名请求
    :param request: 包含重命名规则的POST请求
    :return: 重命名结果
    """
    try:
        data = request.json
        directory = data.get('directory')
        rename_rules = data.get('rename_rules')
        if not directory or not rename_rules:
            abort(400, 'Missing required parameters')
        results = rename_files(directory, rename_rules)
        return response.json(results)
    except Exception as e:
        raise ServerError("Failed to process rename request", e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
