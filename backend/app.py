import os
import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Cross-Origin requests allow karne ke liye (Frontend -> Backend)

# -------------------------
# Menu Data
# -------------------------
menu = [
    {"name": "Masala Tea", "price": 20, "category": "tea", "emoji": "☕", "description": "Fresh Indian Masala Tea"},
    {"name": "Ginger Tea", "price": 20, "category": "tea", "emoji": "🫖", "description": "Hot Adrak Chai"},
    {"name": "Veg Momos", "price": 40, "category": "Momos", "emoji": "🥟", "description": "Steamed / Fried"},
    {"name": "Paneer Momos", "price": 80, "category": "Momos", "emoji": "🧀", "description": "Cheesy Paneer Filling"},
    {"name": "Veg Burger", "price": 60, "category": "snacks", "emoji": "🍔", "description": "Fresh Veg Patty Burger"},
    {"name": "Cheese Maggi", "price": 50, "category": "snacks", "emoji": "🍜", "description": "Loaded with Cheese"},
    {"name": "White Sauce Pasta", "price": 90, "category": "chinese", "emoji": "🍝", "description": "Creamy Italian Style"},
    {"name": "Grilled Sandwich", "price": 70, "category": "snacks", "emoji": "🥪", "description": "Loaded Veg Sandwich"},
    {"name": "Veg Fried Rice", "price": 90, "category": "chinese", "emoji": "🍚", "description": "Chinese Style Rice"},
    {"name": "Veg Chowmein", "price": 80, "category": "chinese", "emoji": "🥡", "description": "Street Style Noodles"},
    {"name": "chicken Chowmein", "price": 100, "category": "chinese", "emoji": "🥡", "description": "chicken Noodles"}
]

# -------------------------
# MySQL Connection Helper (Secure: Reads strictly from Environment Variables)
# -------------------------
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'mysql-0.mysql-service'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME')
    )

# -------------------------
# Health Check API
# -------------------------
@app.route("/")
@app.route("/health")
def health():
    return jsonify({
        "status": "UP"
    })

# -------------------------
# Menu API
# -------------------------
@app.route("/api/menu")
def get_menu():
    return jsonify(menu)

# -------------------------
# Version API
# -------------------------
@app.route("/api/version")
def version():
    return jsonify({
        "application": "Chai Politics",
        "version": "1.0.0",
        "environment": "Production"
    })

# -------------------------
# Cart APIs (Database Driven)
# -------------------------

# 1. Add Item to Cart
@app.route("/api/cart", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid payload!"}), 400

    user_name = data.get("user_name")
    user_email = data.get("user_email")
    user_phone = data.get("user_phone")
    item_name = data.get("item_name")
    price = data.get("price")
    quantity = data.get("quantity", 1)

    # Validation
    if not user_name or not user_email or not user_phone or not item_name or not price:
        return jsonify({"error": "user_name, user_email, user_phone, item_name, and price are required!"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO cart (user_name, user_email, user_phone, item_name, price, quantity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_name, user_email, user_phone, item_name, price, quantity))
        conn.commit()
        
        cursor.close()
        conn.close()
        return jsonify({"message": f"Item added to cart successfully for {user_name}!"}), 201

    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

# 2. Get Cart Items by User Email
@app.route("/api/cart/<string:email>", methods=["GET"])
def get_cart_by_email(email):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM cart WHERE user_email = %s ORDER BY created_at DESC"
        cursor.execute(query, (email,))
        cart_items = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return jsonify(cart_items), 200

    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)