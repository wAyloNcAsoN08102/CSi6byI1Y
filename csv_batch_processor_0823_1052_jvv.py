# 代码生成时间: 2025-08-23 10:52:35
import asyncio
import csv
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.exceptions import ServerError
import os
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Sanic("CSV Batch Processor")

# 定义全局变量
CSV_DIRECTORY = "./csv_files"  # CSV文件目录
PROCESSED_DIRECTORY = "./processed_files"  # 处理后的文件目录

# 确保目录存在
if not os.path.exists(CSV_DIRECTORY):
    os.makedirs(CSV_DIRECTORY)
if not os.path.exists(PROCESSED_DIRECTORY):
    os.makedirs(PROCESSED_DIRECTORY)

# 处理单个CSV文件的函数
async def process_csv_file(file_path):
    try:
        # 打开CSV文件
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            processed_data = []
            # 读取CSV内容
            for row in reader:
                processed_data.append(row)  # 这里可以添加任何处理逻辑
            # 将处理后的数据保存为新文件
            new_file_path = os.path.join(PROCESSED_DIRECTORY, os.path.basename(file_path))
            with open(new_file_path, 'w', newline='') as new_file:
                writer = csv.writer(new_file)
                writer.writerows(processed_data)
        return {
            "status": "success",
            "message": "File processed successfully",
            "file": os.path.basename(file_path)
        }
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {str(e)}")
        return {
            "status": "error",
            "message": f"Error processing file {file_path}: {str(e)}"
        }

# 批量处理CSV文件
@app.route("/process", methods=["POST"])
async def process_csv(request: Request):
    try:
        # 获取上传的CSV文件列表
        files = request.files.getlist("files")
        tasks = [asyncio.create_task(process_csv_file(file.name)) for file in files]
        results = await asyncio.gather(*tasks)
        return response.json(results)
    except Exception as e:
        logger.error(f"Error processing CSV files: {str(e)}")
        raise ServerError("Failed to process CSV files")

# 启动服务
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
