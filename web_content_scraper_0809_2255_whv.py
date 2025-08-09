# 代码生成时间: 2025-08-09 22:55:40
import aiohttp
from sanic import Sanic
from sanic.response import json, html
from sanic.exceptions import ServerError, ClientError
from bs4 import BeautifulSoup

# 网页内容抓取工具的Sanic应用
app = Sanic("WebContentScraper")

# 错误处理
@app.exception(ServerError)
async def server_error(request, exception):
    return json({
        "error": "Internal Server Error",
        "message": str(exception)
    }, status=500)

@app.exception(ClientError)
async def client_error(request, exception):
    return json({
        "error": "Client Error",
        "message": str(exception)
    }, status=400)

# 抓取网页内容的异步函数
async def fetch_web_content(session, url):
    try:
        # 使用aiohttp发起GET请求
        async with session.get(url) as response:
            # 确保请求成功
            response.raise_for_status()
            # 获取网页内容
            content = await response.text()
            return content
    except aiohttp.ClientResponseError as e:
        # 处理HTTP错误
        return {'error': f'HTTP Response Error: {e.status}'}
    except Exception as e:
        # 处理其他异常
        return {'error': str(e)}

# 处理网页内容抓取请求的Sanic路由
@app.route('/scraper/<url:path>', methods=['GET'])
async def scrape_route(request, url):
    # 使用aiohttp创建一个session对象
    async with aiohttp.ClientSession() as session:
        # 调用异步函数抓取网页内容
        content = await fetch_web_content(session, url)
        if 'error' in content:
            # 如果有错误返回JSON错误信息
            return json(content, status=500)
        else:
            # 解析HTML内容
            soup = BeautifulSoup(content, 'html.parser')
            # 提取网页的body部分
            body = soup.body
            # 返回解析后的HTML内容
            return html(str(body))

if __name__ == '__main__':
    # 启动Sanic应用
    app.run(host='0.0.0.0', port=8000, debug=True)