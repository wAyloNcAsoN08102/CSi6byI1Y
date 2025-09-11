# 代码生成时间: 2025-09-12 06:14:53
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound, Unauthorized
from sanic.response import json as sanic_json

# 库存管理系统
app = Sanic('InventoryManagement')

# 模拟库存数据
inventory = {
    'items': [
        {'id': 1, 'name': 'Item1', 'quantity': 100},
        {'id': 2, 'name': 'Item2', 'quantity': 50},
        {'id': 3, 'name': 'Item3', 'quantity': 75}
    ]
}

# 获取所有库存项
@app.route('/api/inventory', methods=['GET'])
async def get_inventory(request):
    """
    Get all inventory items.
    """
    try:
        return sanic_json(inventory['items'])
    except Exception as e:
        raise ServerError("Failed to retrieve inventory", e)

# 获取单个库存项
@app.route('/api/inventory/<item_id:int>', methods=['GET'])
async def get_inventory_item(request, item_id):
    """
    Get a specific inventory item by ID.
    """
    try:
        item = next((item for item in inventory['items'] if item['id'] == item_id), None)
        if not item:
            raise NotFound('Item not found')
        return sanic_json(item)
    except Exception as e:
        raise ServerError("Failed to retrieve item", e)

# 添加库存项
@app.route('/api/inventory', methods=['POST'])
async def add_inventory_item(request):
    """
    Add a new inventory item.
    """
    try:
        data = request.json
        if 'name' not in data or 'quantity' not in data:
            raise Unauthorized('Missing required fields')
        data['id'] = max((item['id'] for item in inventory['items']) or [0]) + 1
        inventory['items'].append(data)
        return sanic_json(data, status=201)
    except Exception as e:
        raise ServerError("Failed to add item", e)

# 更新库存项
@app.route('/api/inventory/<item_id:int>', methods=['PUT'])
async def update_inventory_item(request, item_id):
    """
    Update a specific inventory item by ID.
    """
    try:
        data = request.json
        item = next((item for item in inventory['items'] if item['id'] == item_id), None)
        if not item:
            raise NotFound('Item not found')
        if 'name' in data:
            item['name'] = data['name']
        if 'quantity' in data:
            item['quantity'] = data['quantity']
        return sanic_json(item)
    except Exception as e:
        raise ServerError("Failed to update item", e)

# 删除库存项
@app.route('/api/inventory/<item_id:int>', methods=['DELETE'])
async def delete_inventory_item(request, item_id):
    """
    Delete a specific inventory item by ID.
    """
    try:
        item = next((item for item in inventory['items'] if item['id'] == item_id), None)
        if not item:
            raise NotFound('Item not found')
        inventory['items'] = [item for item in inventory['items'] if item['id'] != item_id]
        return response.text('Item deleted', status=204)
    except Exception as e:
        raise ServerError("Failed to delete item", e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
