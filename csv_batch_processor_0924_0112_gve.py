# 代码生成时间: 2025-09-24 01:12:51
import csv
import os
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound, abort
from sanic.request import Request
from sanic.response import json


# 定义一个类，用于处理CSV文件
class CSVProcessor:
    def __init__(self):
        # 初始化处理程序
        pass

    def process_csv(self, file_path):
        """处理单个CSV文件。"""
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                data = [row for row in reader]
                return data
        except FileNotFoundError:
            raise NotFound('File not found')
        except Exception as e:
            raise ServerError('An error occurred while processing the CSV file', e)

    def process_directory(self, directory_path):
        """处理指定目录下的所有CSV文件。"""
        try:
            csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
            data = {}
            for file in csv_files:
                file_path = os.path.join(directory_path, file)
                data[file] = self.process_csv(file_path)
            return data
        except FileNotFoundError:
            raise NotFound('Directory not found')
        except Exception as e:
            raise ServerError('An error occurred while processing the directory', e)


# 创建Sanic应用
app = Sanic(__name__)

# 定义路由处理函数，用于上传CSV文件
@app.route('/upload', methods=['POST'])
async def upload_csv(request: Request):
    """上传CSV文件。"""
    if 'file' not in request.files:
        return json({'error': 'No file part in the request'}, status=400)

    file = request.files['file']
    if not file.content_type.startswith('text/csv'):
        return json({'error': 'Invalid file type, must be CSV'}, status=400)

    try:
        # 保存文件
        file_path = os.path.join('csv_files', file.name)
        with open(file_path, 'wb') as f:
            f.write(file.body)
    except Exception as e:
        return json({'error': 'An error occurred while saving the file'}, status=500)

    return json({'message': 'File uploaded successfully'})

# 定义路由处理函数，用于处理CSV文件
@app.route('/process', methods=['POST'])
async def process_csv_file(request: Request):
    """处理上传的CSV文件。
    需要JSON请求体，包含文件路径。
    """
    try:
        file_path = request.json.get('file_path')
        if not file_path:
            return json({'error': 'File path is required'}, status=400)

        processor = CSVProcessor()
        result = processor.process_csv(file_path)
        return json({'data': result})
    except NotFound as e:
        return json({'error': str(e)}, status=404)
    except ServerError as e:
        return json({'error': str(e)}, status=500)

# 定义路由处理函数，用于批量处理CSV文件目录
@app.route('/process_directory', methods=['POST'])
async def process_csv_directory(request: Request):
    """批量处理指定目录下的所有CSV文件。
    需要JSON请求体，包含目录路径。
    """
    try:
        directory_path = request.json.get('directory_path')
        if not directory_path:
            return json({'error': 'Directory path is required'}, status=400)

        processor = CSVProcessor()
        result = processor.process_directory(directory_path)
        return json({'data': result})
    except NotFound as e:
        return json({'error': str(e)}, status=404)
    except ServerError as e:
        return json({'error': str(e)}, status=500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)