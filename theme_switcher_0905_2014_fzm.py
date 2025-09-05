# 代码生成时间: 2025-09-05 20:14:28
from sanic import Sanic
from sanic.response import json


# 定义全局变量存储当前主题
current_theme = 'light'

app = Sanic('ThemeSwitcherApp')


@app.listener('before_server_start')
async def setup(app, loop):
    # 在服务器启动前设置主题
    global current_theme
    app.config['current_theme'] = 'light'


@app.route('/api/theme', methods=['GET'])
async def get_theme(request):
    # 获取当前主题
    return json({'theme': app.config.get('current_theme', 'light')})


@app.route('/api/theme', methods=['POST'])
async def set_theme(request):
    # 设置新的主题
    try:
        new_theme = request.json.get('theme')
        if new_theme not in ['light', 'dark']:
            return json({'error': 'Invalid theme'}, status=400)
        global current_theme
        current_theme = new_theme
        app.config['current_theme'] = current_theme
        return json({'theme': current_theme})
    except Exception as e:
        return json({'error': 'Failed to set theme'}, status=500)


if __name__ == '__main__':
    # 启动Sanic服务器
    app.run(host='0.0.0.0', port=8000, workers=1)
