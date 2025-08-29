# 代码生成时间: 2025-08-29 10:42:52
import sanic
from sanic.response import json, file
import csv
import os
from typing import Dict, List

# 定义一个简单的配置类，用于存储配置信息
class Config:
    CSV_DIRECTORY = "./csv_files/"
    OUTPUT_DIRECTORY = "./output_files/"

# CSV处理器类
class CSVProcessor:
    def __init__(self, config: Config):
        self.config = config

    def process_csv_file(self, file_path: str) -> Dict[str, List[str]]:
        """处理单个CSV文件并返回结果"""
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                data = [row for row in reader]
            return {"status": "success", "data": data}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # 处理指定目录下的所有CSV文件
    def process_all_csv_files(self) -> List[Dict[str, List[str] or str]]:
        """处理指定目录下的所有CSV文件"""
        results = []
        for file_name in os.listdir(self.config.CSV_DIRECTORY):
            if file_name.endswith('.csv'):
                file_path = os.path.join(self.config.CSV_DIRECTORY, file_name)
                result = self.process_csv_file(file_path)
                results.append(result)
        return results

# 创建Sanic应用
app = sanic.Sanic("CSV Batch Processor")

# 路由：处理CSV文件
@app.route("/process_csv", methods=["POST"])
async def process_csv(request: sanic.Request):
    file = request.files.get("file")
    if not file:
        return json({"error": "No file provided"}, status=400)

    csv_processor = CSVProcessor(Config())
    result = csv_processor.process_csv_file(file.file)
    return json(result)

# 路由：处理目录下所有CSV文件
@app.route("/process_all_csv", methods=["GET"])
async def process_all_csv(request: sanic.Request):
    csv_processor = CSVProcessor(Config())
    results = csv_processor.process_all_csv_files()
    return json(results)

# 启动Sanic应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)