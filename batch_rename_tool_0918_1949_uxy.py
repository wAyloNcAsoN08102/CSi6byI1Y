# 代码生成时间: 2025-09-18 19:49:55
import os
from sanic import Sanic, response
def rename_files(directory, rename_pattern):
    # 这个函数用于根据指定的模式重命名指定目录中的文件
    for filename in os.listdir(directory):
        try:
            new_filename = rename_pattern.format(filename)
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            os.rename(old_path, new_path)
            print(f'Renamed {filename} to {new_filename}')
        except Exception as e:
            print(f'Failed to rename {filename} due to {e}')

app = Sanic('BatchRenameTool')

@app.route('/api/rename', methods=['POST'])
async def rename(request):
    # API端点，接收重命名请求
    directory = request.json.get('directory')
    rename_pattern = request.json.get('rename_pattern')
    if not directory or not rename_pattern:
        return response.json({'error': 'Missing directory or rename pattern'})
    try:
        rename_files(directory, rename_pattern)
        return response.json({'message': 'Renaming completed successfully'})
    except Exception as e:
        return response.json({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
