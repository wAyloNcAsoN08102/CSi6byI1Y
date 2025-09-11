# 代码生成时间: 2025-09-11 12:22:57
import asyncio
import zipfile
import sanic
from sanic.request import Request
from sanic.response import file as file_response
def unzip_file(zip_path, extract_dir):
    """解压缩ZIP文件到指定目录"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        return f"Files extracted to {extract_dir}"
    except Exception as e:
        return f"An error occurred: {e}"

class DecompressionApp:
    def __init__(self):
        self.app = sanic.Sanic("DecompressionApp")
        self.app.add_route(self.upload_zip, "/upload", methods=["POST"])
        self.app.add_route(self.get解压_files, "/files", methods=["GET"])

    def upload_zip(self, request: Request):
        """上传ZIP文件并解压"""
        if "file" not in request.files:
            return sanic.response.json({"error": "No file provided"}, status=400)

        file = request.files["file"]
        zip_path = f"./tmp/{file.name}"
        with open(zip_path, "wb") as f:
            f.write(file.body)

        extract_dir = "./extracted"
        result = unzip_file(zip_path, extract_dir)
        return sanic.response.json({"message": result})

    def get解压_files(self, request: Request):
        """获取解压后的文件列表"""
        extract_dir = "./extracted"
        try:
            files = [f for f in os.listdir(extract_dir)]
            return sanic.response.json({"files": files})
        except Exception as e:
            return sanic.response.json({"error": f"An error occurred: {e}"}, status=500)

    def run(self):
        "