# 代码生成时间: 2025-09-14 22:51:49
import os
from sanic import Sanic, response
from sanic.request import Request
from sanic.exceptions import ServerError, Unauthorized, NotFound
from PIL import Image

# 定义应用
app = Sanic('ImageResizer')

# 存储配置
config = {
    'target_size': (800, 600),  # 目标尺寸
    'output_folder': 'resized_images',  # 输出文件夹
    'allowed_extensions': ['.jpg', '.jpeg', '.png', '.bmp']  # 允许的文件类型
}

# 路由：上传图片并调整尺寸
@app.route('/upload', methods=['POST'])
async def resize_image(request: Request):
    try:
        # 检查请求是否包含文件
        if 'file' not in request.files:
            raise NotFound('No file part in the request')

        file = request.files['file']
        if not file:
            raise NotFound('No file in the request')

        # 检查文件扩展名
        if file.name.split('.')[-1].lower() not in config['allowed_extensions']:
            raise Unauthorized(f'Unsupported file type: {file.name}')

        # 读取图片
        image = Image.open(file.file)

        # 调整图片尺寸
        image = image.resize(config['target_size'], Image.ANTIALIAS)

        # 保存调整后的图片
        output_path = os.path.join(config['output_folder'], file.name)
        image.save(output_path)

        # 返回成功响应
        return response.json({'message': 'Image resized successfully', 'path': output_path})
    except Exception as e:
        # 错误处理
        raise ServerError(f'Failed to resize image: {str(e)}')

# 运行应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
