# 代码生成时间: 2025-10-07 21:30:43
import asyncio
from sanic import Sanic
from sanic.response import json, text
from sanic.exceptions import ServerError
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import NotFoundError, RequestError

# 商品搜索引擎服务
app = Sanic("ProductSearchService")

# Elasticsearch配置
ES_HOST = "localhost"
ES_PORT = 9200
ES_INDEX = "products"

# 初始化Elasticsearch客户端
es_client = Elasticsearch([{"host": ES_HOST, "port": ES_PORT}])

# 定义错误处理
@app.exception(NotFoundError, RequestError)
async def handle_es_errors(request, exception):
    return json({"error": str(exception)}, status=500)

# 商品搜索路由
@app.route("/search", methods=["GET"])
async def search_products(request):
    # 获取查询参数
    query = request.args.get("query", None)
    if query is None:
        return json({"error": "Missing query parameter"}, status=400)

    try:
        # 构建Elasticsearch查询体
        body = {
            "query": {
                "match": {
                    "product_name": query
                }
            }
        }

        # 执行搜索
        response = es_client.search(index=ES_INDEX, body=body)

        # 提取搜索结果
        hits = response["hits"]["hits"]
        products = [hit["_source"] for hit in hits]

        # 返回搜索结果
        return json(products)
    except (NotFoundError, RequestError) as e:
        # 异常处理
        raise ServerError(e)

    except Exception as e:
        # 处理其他异常
        return json({"error": "Internal Server Error"}, status=500)

# 程序入口点
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
