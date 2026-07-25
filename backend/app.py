import os
import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

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
    {"name": "Chicken Chowmein", "price": 100, "category": "chinese", "emoji": "🥡", "description": "Chicken Noodles"}
]

# -------------------------
# Database Helper
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
    return jsonify({"status": "UP"})

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
# User Authentication APIs
# -------------------------

# 1. Existing User Login Route (Phone only)
@app.route("/api/login", methods=["POST"])
def login_user():
    data = request.get_json(silent=True) or {}
    phone = data.get("phone", "").strip()

    if not phone:
        return jsonify({"error": "Phone number is required!"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, name, phone FROM users WHERE phone = %s", (phone,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            return jsonify({"error": "Account not found. Please register first."}), 404

        return jsonify({
            "message": "Login successful!",
            "user_id": user["id"],
            "name": user["name"],
            "phone": user["phone"]
        }), 200

    except Exception as e:
        print(f"Login Error: {str(e)}", flush=True)
        return jsonify({"error": "Database error", "details": str(e)}), 500


# 2. New User Registration Route (Name & Phone)
@app.route("/api/register", methods=["POST"])
def register_user():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()

    if not name or not phone:
        return jsonify({"error": "Name and phone number are required!"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check existing user
        cursor.execute("SELECT id, name, phone FROM users WHERE phone = %s", (phone,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()
            return jsonify({"error": "Phone number already registered. Please login."}), 409

        # Register user without relying on optional email column
        cursor.execute("INSERT INTO users (name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        user_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Registration successful!",
            "user_id": user_id,
            "name": name,
            "phone": phone
        }), 201

    except Exception as e:
        print(f"Register Error: {str(e)}", flush=True)
        return jsonify({"error": "Database error", "details": str(e)}), 500

# -------------------------
# Cart Operations APIs
# -------------------------

# 1. Add Item to Cart
@app.route("/api/cart", methods=["POST"])
def add_to_cart():
    data = request.get_json(silent=True) or {}
    user_phone = data.get("user_phone", "").strip()
    item_name = data.get("item_name", "").strip()
    price = data.get("price")
    quantity = data.get("quantity", 1)

    if not user_phone or not item_name or price is None:
        return jsonify({"error": "user_phone, item_name, and price are required!"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, name FROM users WHERE phone = %s", (user_phone,))
        user = cursor.fetchone()

        if not user:
            cursor.close()
            conn.close()
            return jsonify({"error": "User not registered!"}), 401

        query = """
            INSERT INTO cart (user_id, user_name, user_phone, item_name, price, quantity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user["id"], user["name"], user_phone, item_name, price, quantity))
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"message": f"Added {item_name} to cart!"}), 201

    except Exception as e:
        print(f"Add Cart Error: {str(e)}", flush=True)
        return jsonify({"error": "Database error", "details": str(e)}), 500


# 2. Get Cart Items
@app.route("/api/cart/<string:phone>", methods=["GET"])
def get_cart_by_phone(phone):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM cart WHERE user_phone = %s ORDER BY created_at DESC"
        cursor.execute(query, (phone,))
        cart_items = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify(cart_items), 200

    except Exception as e:
        print(f"Get Cart Error: {str(e)}", flush=True)
        return jsonify({"error": "Database error", "details": str(e)}), 500


# 3. Clear Cart (Checkout)
@app.route("/api/cart/<string:phone>", methods=["DELETE"])
def clear_cart(phone):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM cart WHERE user_phone = %s", (phone,))
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"message": "Cart cleared successfully!"}), 200

    except Exception as e:
        print(f"Clear Cart Error: {str(e)}", flush=True)
        return jsonify({"error": "Database error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)