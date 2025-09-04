# 代码生成时间: 2025-09-04 15:36:47
import sanic
# 添加错误处理
from sanic.response import json, html
from sanic.exceptions import ServerError, NotFound
from jinja2 import Environment, FileSystemLoader
import plotly.express as px
import pandas as pd

# 配置Jinja2模板引擎
env = Environment(loader=FileSystemLoader("templates"))

app = sanic.Sanic("InteractiveChartGenerator")

# 定义图表数据和类型
CHART_TYPES = {
    "line": px.line,
    "bar": px.bar,
    "scatter": px.scatter
}

# 定义路由来提供首页界面
@app.route("/", methods=["GET"])
async def home(request):
    # 加载首页模板
    template = env.get_template('home.html')
    return html(template.render())

# 定义路由来接收图表数据并生成图表
# 改进用户体验
@app.route("/generate-chart", methods=["POST"])
async def generate_chart(request):
    try:
        # 获取请求体中的数据
        data = request.json
        chart_type = data.get("type")
        df_data = data.get("data")
# 扩展功能模块
        
        # 检查图表类型和数据
        if chart_type not in CHART_TYPES:
            raise ValueError("Unsupported chart type")
# NOTE: 重要实现细节
        if not df_data:
            raise ValueError("No data provided")
        
        # 将数据转换为Pandas DataFrame
        df = pd.DataFrame(df_data)
        
        # 生成图表
        chart = CHART_TYPES[chart_type](df, **data.get("args", {}))
        
        # 转换为HTML以嵌入网页
        html_div = chart.to_html(full_html=False)
        return json({"status": "success", "chart": html_div})
    except ValueError as e:
        return json({"status": "error", "message": str(e)})
    except Exception as e:
        raise ServerError("Server error occurred while generating chart")

# 运行应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
