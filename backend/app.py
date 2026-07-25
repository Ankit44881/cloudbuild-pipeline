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
# User Login / Registration API
# -------------------------
@app.route("/api/login", methods=["POST"])
def login_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid payload!"}), 400

    name = data.get("name")
    phone = data.get("phone")
    email = data.get("email", "")

    if not name or not phone:
        return jsonify({"error": "Name and phone are required!"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if user already exists by unique phone number
        cursor.execute("SELECT * FROM users WHERE phone = %s", (phone,))
        user = cursor.fetchone()

        if not user:
            # Register new user
            cursor.execute(
                "INSERT INTO users (name, phone, email) VALUES (%s, %s, %s)",
                (name, phone, email)
            )
            conn.commit()
            user_id = cursor.lastrowid
        else:
            user_id = user["id"]

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Login successful!",
            "user_id": user_id,
            "name": name,
            "phone": phone
        }), 200

    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

# -------------------------
# Cart APIs (Database Driven)
# -------------------------

# 1. Add Item to Cart
@app.route("/api/cart", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid payload!"}), 400

    user_phone = data.get("user_phone")
    item_name = data.get("item_name")
    price = data.get("price")
    quantity = data.get("quantity", 1)

    # Validation
    if not user_phone or not item_name or not price:
        return jsonify({"error": "user_phone, item_name, and price are required!"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verify user exists using phone number
        cursor.execute("SELECT id, name FROM users WHERE phone = %s", (user_phone,))
        user = cursor.fetchone()

        if not user:
            cursor.close()
            conn.close()
            return jsonify({"error": "User not registered or logged in!"}), 401

        # Insert item into cart linked with user_id
        query = """
            INSERT INTO cart (user_id, user_name, user_phone, item_name, price, quantity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user["id"], user["name"], user_phone, item_name, price, quantity))
        conn.commit()
        
        cursor.close()
        conn.close()
        return jsonify({"message": f"Item added to cart successfully for {user['name']}!"}), 201

    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

# 2. Get Cart Items by User Phone Number
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
        return jsonify({"error": "Database error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)