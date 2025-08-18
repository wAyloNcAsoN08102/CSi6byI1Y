# 代码生成时间: 2025-08-19 00:31:07
import asyncio
from sanic import Sanic
from sanic.response import json

# 创建一个Sanic应用
app = Sanic('SortingService')

# 一个简单的冒泡排序函数
async def bubble_sort(arr):
    """
    进行冒泡排序的异步函数。
    :param arr: 待排序的数组
    :return: 排序后的数组
    """
    n = len(arr)
    # 遍历数组中的每个元素
    for i in range(n):
        # 最后i个元素已经是排好序的了，不需要再比较
        for j in range(0, n-i-1):
            # 遍历数组从0到n-i-1
            if arr[j] > arr[j+1]:
                # 交换两个元素的位置
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# 排序服务端点
@app.route('/sort', methods=['POST'])
async def sort(request):
    """
    接受一个JSON数组并返回排序后的数组。
    :param request: 包含待排序数组的请求对象
    :return: 排序后的数组
    """
    try:
        data = request.json
        if not isinstance(data, list):
            return json({'error': 'Provided data is not a list'}, status=400)

        sorted_data = await bubble_sort(data)
        return json({'sorted_array': sorted_data})
    except Exception as e:
        return json({'error': str(e)}, status=500)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)