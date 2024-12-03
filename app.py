import os
import base64
import time
import requests  # To send data to Telegram API
from flask import Flask, render_template, request, jsonify
from helpers import file_upload
from routers import (
    dashboard_router,
    user_router,
    product_router,
    category_router,
    brand_router,
    tag_router,
    unit_router,
    router
)
from db.database import init_db

# Create the Flask app
app = Flask(__name__)

# Define the image directory and create it if it doesn't exist
IMAGE_DIR = 'static/uploaded_images'
app.config['IMAGE_DIR'] = IMAGE_DIR  # Store it in the app config
os.makedirs(IMAGE_DIR, exist_ok=True)

# Define the Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

@app.post('/upload')
def upload():
    base64_string = request.json.get('image')
    if not base64_string:
        return {"error": "No image provided"}, 400

    name = f"{time.time()}.png"
    image_path = os.path.join(IMAGE_DIR, name)
    
    try:
        with open(image_path, 'wb') as img_file:
            img_file.write(base64.b64decode(base64_string.split(',')[1]))
    except Exception as e:
        print("File saving error:", e)
        return {"error": "Failed to save image"}, 500

    return {"message": "Image uploaded successfully", "path": image_path}, 201

@app.route('/homepage')
def home():
    return render_template('/views/index.html')

@app.route('/payment')
def cart():
    return render_template('/views/payment.html')

@app.route('/productview')
def productview():
    return render_template('/views/productview.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    # Get the data from the frontend
    data = request.json
    name = data.get('name')
    phone_number = data.get('phone_number')
    email = data.get('email')
    address = data.get('address')
    product_name = data.get('productName')
    product_price = data.get('productPrice')
    product_quantity = data.get('productQuantity')
    total_price = data.get('totalPrice')

    # Format the message for Telegram
    message = f"""
🛎 New Order Confirmation 🛎

👤 Name: {name}
📞 Phone: {phone_number}
📧 Email: {email}
🏠 Address: {address}

--------------------------------------
📅 Booking Date: {time.strftime('%Y-%m-%d %H:%M:%S')}
--------------------------------------

📦 Items:
{product_name} (Quantity: {product_quantity}, Price: ${product_price:.2f})

💵 Total Price: ${total_price:.2f}

🎉 Thank you for your support! 🎉
    """

    # Send the message to Telegram using the Telegram Bot API
    try:
        response = requests.post(
            f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
            data={
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message
            }
        )
        
        # Check if the message was sent successfully
        if response.status_code == 200:
            return jsonify({"message": "Order sent successfully!"}), 200
        else:
            return jsonify({"error": "Failed to send message to Telegram."}), 500
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")
        return jsonify({"error": "An error occurred while sending the message."}), 500

# Initialize the database (create tables if they do not exist)
init_db()

# Register blueprints for routing
app.register_blueprint(dashboard_router)
app.register_blueprint(user_router)
app.register_blueprint(product_router)
app.register_blueprint(category_router)
app.register_blueprint(brand_router)
app.register_blueprint(tag_router)
app.register_blueprint(unit_router)
app.register_blueprint(router)

if __name__ == '__main__':
    app.run(debug=True)
