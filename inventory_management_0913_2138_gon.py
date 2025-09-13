# 代码生成时间: 2025-09-13 21:38:16
from sanic import Sanic, response
from sanic.response import json
from sanic.exceptions import ServerError, NotFound
import json as json_module

# Inventory management system
class InventoryManager:
    def __init__(self):
        self.inventory = {}

    def add_item(self, item, quantity):
        """Add item to the inventory."""
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity

    def remove_item(self, item, quantity):
        """Remove item from the inventory."""
        if item not in self.inventory:
            raise NotFound("Item not found in inventory")
        if self.inventory[item] < quantity:
            raise ServerError("Not enough quantity available")
        self.inventory[item] -= quantity
        if self.inventory[item] == 0:
            del self.inventory[item]

    def get_inventory(self):
        """Return the current inventory."""
        return self.inventory

    def get_item(self, item):
        """Return the quantity of a specific item."""
        return self.inventory.get(item, 0)


# Sanic application
app = Sanic("Inventory Management")
inventory_manager = InventoryManager()

# API endpoints
@app.route("/add", methods=["POST"])
async def add_item(request):
    data = request.json
    item = data.get("item")
    quantity = data.get("quantity", 0)
    if not isinstance(quantity, int):
        return response.json({
            "error": "Invalid quantity"
        }, status=400)
    try:
        inventory_manager.add_item(item, quantity)
        return response.json({
            "success": f"Added {quantity} of {item} to inventory"
        })
    except Exception as e:
        return response.json({
            "error": str(e)
        }, status=500)

@app.route("/remove", methods=["POST"])
async def remove_item(request):
    data = request.json
    item = data.get("item")
    quantity = data.get("quantity", 0)
    if not isinstance(quantity, int):
        return response.json({
            "error": "Invalid quantity"
        }, status=400)
    try:
        inventory_manager.remove_item(item, quantity)
        return response.json({
            "success": f"Removed {quantity} of {item} from inventory"
        })
    except NotFound as e:
        return response.json({
            "error": str(e)
        }, status=404)
    except ServerError as e:
        return response.json({
            "error": str(e)
        }, status=500)
    except Exception as e:
        return response.json({
            "error": str(e)
        }, status=500)

@app.route("/inventory")
async def get_inventory(request):
    try:
        return response.json(inventory_manager.get_inventory())
    except Exception as e:
        return response.json({
            "error": str(e)
        }, status=500)

@app.route("/item/<item>")
async def get_item(request, item):
    try:
        quantity = inventory_manager.get_item(item)
        if quantity == 0:
            raise NotFound(f"Item {item} not found in inventory")
        return response.json({
            "item": item,
            "quantity": quantity
        })
    except NotFound as e:
        return response.json({
            "error": str(e)
        }, status=404)
    except Exception as e:
        return response.json({
            "error": str(e)
        }, status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)