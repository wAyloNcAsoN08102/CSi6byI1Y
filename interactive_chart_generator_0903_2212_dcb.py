# 代码生成时间: 2025-09-03 22:12:54
import asyncio
from sanic import Sanic, response
from sanic.response import json as sanic_json
from sanic.exceptions import ServerError, NotFound
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# 初始化Sanic应用
app = Sanic("InteractiveChartGenerator")

# 定义路由和视图函数
@app.route("/generate", methods=["POST"])
async def generate_chart(request):
    """
    生成交互式图表。
    
    参数：
    - request: Sanic的请求对象，包含图表数据。
    
    返回：
    - HTTP响应，包含图表的图片数据。
    """
    try:
        # 解析请求数据
        data = request.json
        
        # 验证数据
        if 'data' not in data or 'chart_type' not in data:
            return sanic_json({'error': 'Invalid data'}, 400)
        
        # 创建Pandas DataFrame
        df = pd.DataFrame(data['data'])
        
        # 根据图表类型生成图表
        if data['chart_type'] == 'line':
            chart = plt.figure()
            plt.plot(df)
        elif data['chart_type'] == 'bar':
            chart = plt.figure()
            plt.bar(df)
        else:
            return sanic_json({'error': 'Unsupported chart type'}, 400)
        
        # 保存图表为图片
        img_buffer = BytesIO()
        chart.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        
        # 编码图片为Base64
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
        # 返回图片数据
        return sanic_json({'chart': 'data:image/png;base64,' + img_base64})
    except Exception as e:
        # 错误处理
        raise ServerError('Failed to generate chart', 'Internal Server Error', 500)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)