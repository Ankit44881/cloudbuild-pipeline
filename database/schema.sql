USE chaipolitics_db;

-- 1. Create Users Table with Strict Indian Phone Number Constraint
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(10) NOT NULL UNIQUE,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- DB Level Enforcement:
    -- 1. Must be exactly 10 digits
    -- 2. Must start with 6, 7, 8, or 9
    -- 3. Rejects alphabets, special characters, and spaces
    CONSTRAINT chk_indian_phone CHECK (phone REGEXP '^[6-9][0-9]{9}$')
);

-- 2. Cart Table (Linked via user_id foreign key)
CREATE TABLE IF NOT EXISTS cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quantity INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);