# 代码生成时间: 2025-10-13 03:03:37
from sanic import Sanic
from sanic.response import json

# Define the DiscountService class to handle discount logic
class DiscountService:
    def __init__(self):
        # A dictionary to store discount rates for different products
        self.discount_rates = {
            'product1': 0.10,  # 10% discount
            'product2': 0.20,  # 20% discount
            'product3': 0.15   # 15% discount
        }

    def apply_discount(self, product, price):
        """
        Apply a discount to the given product price.
        :param product: str - Name of the product
        :param price: float - Original price of the product
        :return: dict - Discounted price and discount amount
        """
        try:
            discount_rate = self.discount_rates[product]
            discounted_price = price * (1 - discount_rate)
            discount_amount = price - discounted_price
            return {'discounted_price': discounted_price, 'discount_amount': discount_amount}
        except KeyError:
            return {'error': 'Product not found'}

# Create the Sanic app
app = Sanic("DiscountServiceApp")

# Initialize the DiscountService
discount_service = DiscountService()

# Define the route to apply discount
@app.route("/apply-discount", methods=["POST"])
async def apply_discount_request(request):
    """
    Handle POST request to apply discount.
    :param request: Sanic request object
    :return: JSON response with the discounted price
    """
    # Extract product name and price from the request body
    product = request.json.get('product')
    price = request.json.get('price')
    if not product or not price:
        return json({'error': 'Product and price are required'}, status=400)

    try:
        price = float(price)
    except ValueError:
        return json({'error': 'Invalid price'}, status=400)

    # Apply the discount using the DiscountService
    result = discount_service.apply_discount(product, price)
    return json(result)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)