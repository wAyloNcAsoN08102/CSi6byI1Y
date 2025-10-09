# 代码生成时间: 2025-10-09 20:44:45
import sanic
from sanic.response import json, text
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import base64
import io
import os
import hmac
import hashlib

"""
Digital Watermarking Service using Sanic framework.

This service allows to embed a watermark into an image.
"""

app = sanic.Sanic('digital_watermarking_service')

def generate_watermark(data: str) -> Image:
    """Generate a watermark image from the given data."""
    font = ImageFont.load_default()
    image = Image.new('RGB', (100, 50), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), data, font=font, fill=(0, 0, 0))
    return image

@app.route('/embed', methods=['POST'])
async def embed_watermark(request):
    """Endpoint to embed a watermark into an image."""
    if 'image' not in request.files or 'watermark' not in request.form:
        return json({'error': 'Missing image or watermark data.'}, status=400)

    image_file = request.files['image']
    watermark_data = request.form['watermark']

    # Validate image and watermark data
    if not image_file.body:
        return json({'error': 'Invalid image file.'}, status=400)
    if not watermark_data:
        return json({'error': 'Watermark data cannot be empty.'}, status=400)

    try:
        # Open the image and convert it to an editable format
        image = Image.open(io.BytesIO(image_file.body)).convert('RGB')
    except IOError:
        return json({'error': 'Invalid image format.'}, status=400)

    # Generate the watermark image
    watermark_image = generate_watermark(watermark_data)
    # Resize watermark to fit the bottom right corner of the image
    watermark_image = watermark_image.resize((image.width // 4, image.height // 4))
    watermark_position = (image.width - watermark_image.width, image.height - watermark_image.height)

    # Paste the watermark onto the image
    image.paste(watermark_image, watermark_position, watermark_image)

    # Save the image with the watermark to a buffer
    image_buffer = io.BytesIO()
    image.save(image_buffer, format='PNG')
    image_buffer.seek(0)

    # Return the image as a response
    return text(image_buffer.read().decode('base64'), content_type='image/png;base64')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
