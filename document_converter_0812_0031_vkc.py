# 代码生成时间: 2025-08-12 00:31:48
import json
from sanic import Sanic, response
from sanic.log import logger
from sanic.exceptions import ServerError
from docx import Document
from docx.shared import Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# 初始化Sanic应用
app = Sanic("DocumentConverter")

# 定义路由处理函数，用于文档转换
@app.route("/convert", methods=["POST"])
async def convert_document(request):
    # 获取上传的文件
    file = request.files.get("file")
    if file is None:
        return response.json(
            {
                "error": "No file provided for conversion."
            },
            status=400,
        )

    try:
        # 将文件保存到临时路径
        file_path = "temp_{}.docx".format(file.filename)
        with open(file_path, "wb") as f:
            f.write(file.body)

        # 打开文档并进行转换（示例为将DOCX转换为RTF）
        doc = Document(file_path)
        doc.save("temp_{}.rtf".format(file.filename))

        # 返回转换后的文件
        with open("temp_{}.rtf".format(file.filename), "rb") as f:
            return response.file(
                "temp_{}.rtf".format(file.filename),
                headers={"Content-Disposition": f'attachment; filename="document.rtf"'},
            )
    except Exception as e:
        logger.error(f"Error converting document: {e}")
        return response.json(
            {
                "error": "Failed to convert document."
            },
            status=500,
        )
    finally:
        # 清理临时文件
        import os
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists("temp_{}.rtf".format(file.filename)):
            os.remove("temp_{}.rtf".format(file.filename))

# 运行Sanic应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)