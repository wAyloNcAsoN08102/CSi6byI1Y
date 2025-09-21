# 代码生成时间: 2025-09-21 13:48:16
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.request import Request
from sanic.response import HTTPResponse

# 定义一个Sanic蓝图
app = Sanic("TestReportGenerator")

# 模板路径
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# 定义Jinja2模板
TEMPLATE = env.get_template('test_report.html')

@app.route("/generate", methods=["GET"])
async def generate_test_report(request: Request):
    """
    生成测试报告的视图函数
    :param request: HTTP请求对象
    :return: 生成的测试报告HTML页面
    """
    try:
        # 从请求中获取必要的参数
        test_name = request.args.get('test_name', default='')
        if not test_name:
            return response.json(
                {'error': 'Missing test_name parameter'}, status=400
            )

        # 生成报告内容
        report_content = {
            'test_name': test_name,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'results': [
                {'test': 'Test1', 'result': 'Passed'},
                {'test': 'Test2', 'result': 'Failed'},
                # 更多测试结果...
            ],
        }

        # 使用模板生成HTML
        html_report = TEMPLATE.render(report_content)

        # 返回HTML响应
        return response.html(html_report)

    except Exception as e:
        # 捕获异常并返回错误信息
        app.log.error("Error generating test report: %s", str(e))
        return response.json({'error': 'Failed to generate test report'}, status=500)

if __name__ == '__main__':
    # 运行Sanic应用
    app.run(host='0.0.0.0', port=8000, debug=True)