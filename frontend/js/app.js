// ==========================================
// 0. On-Screen UI Error Display Helpers
// ==========================================
function showAuthError(message) {
    const errorBox = document.getElementById('authErrorMsg');
    if (errorBox) {
        errorBox.innerText = message;
        errorBox.style.display = 'block';
    }
}

function clearAuthError() {
    const errorBox = document.getElementById('authErrorMsg');
    if (errorBox) {
        errorBox.innerText = '';
        errorBox.style.display = 'none';
    }
}

// Detailed Phone Validation Logic (Syntax error fixed)
function validateIndianPhone(phone) {
    if (!phone) {
        return { valid: false, message: "⚠️ Phone number is required. Please enter your phone number." };
    }

    // Check for Alphabets
    if (/[a-zA-Z]/.test(phone)) {
        return { valid: false, message: "⚠️ Alphabets are not allowed! Please enter numbers only." };
    }

    // Check for Special Characters or Spaces
    if (/[^\d]/.test(phone)) {
        return { valid: false, message: "⚠️ Special characters or spaces are not allowed! Use numbers only." };
    }

    // Check for Short Length
    if (phone.length < 10) {
        return { valid: false, message: `⚠️ Phone number is too short (${phone.length}/10 digits). Please enter a full 10-digit number.` };
    }

    // Check for Excess Length
    if (phone.length > 10) {
        return { valid: false, message: `⚠️ Phone number is too long (${phone.length} digits). Please enter only a 10-digit number.` };
    }

    // Check for valid Indian starting digit (6, 7, 8, or 9)
    if (!/^[6-9]/.test(phone)) {
        return { valid: false, message: "⚠️ Invalid Indian phone number! Must start with 6, 7, 8, or 9." };
    }

    return { valid: true };
}

// ==========================================
// 1. Session and Cart State Helper
// ==========================================
function getUserSession() {
    return {
        name: localStorage.getItem('cp_user_name'),
        phone: localStorage.getItem('cp_user_phone')
    };
}

// ==========================================
// 2. Page Load Initializer
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    updateNavbarUI();
    fetchCartCount();
});

// ==========================================
// 3. Navbar UI Sync Across Pages
// ==========================================
function updateNavbarUI() {
    const session = getUserSession();
    const navUl = document.querySelector('nav ul');
    
    if (!navUl) return;

    // Remove existing dynamic auth/cart elements if any
    const existingAuth = document.getElementById('navAuthItem');
    if (existingAuth) existingAuth.remove();

    const li = document.createElement('li');
    li.id = 'navAuthItem';

    if (session.phone) {
        li.innerHTML = `
            <button class="cart-nav-btn" onclick="openCartModal()">
                🛒 Cart <span id="cartCountBadge" class="cart-badge">0</span>
            </button>
            <button onclick="logoutUser()" style="background:none; border:none; color:#888; cursor:pointer; margin-left:10px;">Logout</button>
        `;
    } else {
        li.innerHTML = `
            <button class="cart-nav-btn" onclick="openLoginModal()">
                🔑 Login / Register
            </button>
        `;
    }
    navUl.appendChild(li);
}

// ==========================================
// 4. Modal Tab Switcher (Login vs Register)
// ==========================================
function switchAuthTab(tab) {
    clearAuthError(); // Clear any previous errors on tab change

    const loginForm = document.getElementById('loginFormSection');
    const regForm = document.getElementById('regFormSection');
    const loginBtn = document.getElementById('loginTabBtn');
    const regBtn = document.getElementById('regTabBtn');

    if (!loginForm || !regForm) return;

    if (tab === 'login') {
        loginForm.style.display = 'block';
        regForm.style.display = 'none';
        
        loginBtn.style.background = '#ff6600';
        loginBtn.style.color = 'white';
        loginBtn.style.border = 'none';

        regBtn.style.background = '#f5f5f5';
        regBtn.style.color = '#333';
        regBtn.style.border = '1px solid #ccc';
    } else {
        loginForm.style.display = 'none';
        regForm.style.display = 'block';

        regBtn.style.background = '#0284c7';
        regBtn.style.color = 'white';
        regBtn.style.border = 'none';

        loginBtn.style.background = '#f5f5f5';
        loginBtn.style.color = '#333';
        loginBtn.style.border = '1px solid #ccc';
    }
}

// ==========================================
// 5. Existing User Login Action (Mapped to /api/users)
// ==========================================
async function handleLogin(event) {
    event.preventDefault();
    clearAuthError();

    const phone = document.getElementById('loginPhone').value.trim();

    // On-Screen Validation Check
    const check = validateIndianPhone(phone);
    if (!check.valid) {
        showAuthError(check.message);
        return;
    }

    try {
        const response = await fetch('/api/users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: 'Chai Lover', phone }) // Default fallback name if not provided
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('cp_user_name', data.user.name);
            localStorage.setItem('cp_user_phone', data.user.phone);
            closeLoginModal();
            updateNavbarUI();
            fetchCartCount();
            alert(`Welcome back, ${data.user.name}!`);
        } else {
            showAuthError(data.error || "Login failed");
        }
    } catch (err) {
        console.error("Login Error:", err);
        showAuthError("Server error during login. Please try again.");
    }
}

// ==========================================
// 6. New User Registration Action (Mapped to /api/users)
// ==========================================
async function handleRegister(event) {
    event.preventDefault();
    clearAuthError();

    const name = document.getElementById('regName').value.trim();
    const phone = document.getElementById('regPhone').value.trim();

    if (!name) {
        showAuthError("⚠️ Please enter your Full Name.");
        return;
    }

    // On-Screen Validation Check
    const check = validateIndianPhone(phone);
    if (!check.valid) {
        showAuthError(check.message);
        return;
    }

    try {
        const response = await fetch('/api/users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, phone })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('cp_user_name', data.user.name);
            localStorage.setItem('cp_user_phone', data.user.phone);
            closeLoginModal();
            updateNavbarUI();
            fetchCartCount();
            alert("🎉 Account created successfully!");
        } else {
            showAuthError(data.error || "Registration failed");
        }
    } catch (err) {
        console.error("Registration Error:", err);
        showAuthError("Server error during registration. Please try again.");
    }
}

// ==========================================
// 7. Add to Cart Logic
// ==========================================
async function addToCart(itemName, price) {
    const session = getUserSession();

    if (!session.phone) {
        openLoginModal();
        return;
    }

    try {
        const response = await fetch('/api/cart', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: session.phone,
                item_name: itemName,
                price: price,
                quantity: 1
            })
        });

        if (response.ok) {
            fetchCartCount();
            alert(`${itemName} added to cart!`);
        } else {
            const errData = await response.json();
            alert(errData.error || "Could not add item.");
        }
    } catch (err) {
        console.error("Cart Add Error:", err);
    }
}

// ==========================================
// 8. Fetch Cart Details by Phone Number
// ==========================================
async function fetchCartCount() {
    const session = getUserSession();
    if (!session.phone) return;

    try {
        const res = await fetch(`/api/cart/${session.phone}`);
        if (!res.ok) return;

        const items = await res.json();
        renderCartModalItems(items);
    } catch (err) {
        console.error("Fetch Cart Error:", err);
    }
}

// ==========================================
// 9. Render Cart Modal Data
// ==========================================
function renderCartModalItems(items) {
    const badge = document.getElementById('cartCountBadge');
    const list = document.getElementById('cartItemsList');
    const total = document.getElementById('cartTotalAmount');

    if (badge) badge.innerText = items.length;
    if (!list) return;

    list.innerHTML = '';
    let sum = 0;

    if (items.length === 0) {
        list.innerHTML = '<li style="text-align:center; padding:15px; color:#666;">Cart is empty</li>';
        if (total) total.innerText = '₹0.00';
        return;
    }

    items.forEach(item => {
        const itemPrice = parseFloat(item.price || 0);
        sum += itemPrice * (item.quantity || 1);

        const li = document.createElement('li');
        li.className = 'cart-item-row';
        li.innerHTML = `
            <div>
                <strong>${item.item_name}</strong>
            </div>
            <div>
                <span style="color:#ff6600; font-weight:bold;">₹${itemPrice.toFixed(2)}</span>
            </div>
        `;
        list.appendChild(li);
    });

    if (total) total.innerText = '₹' + sum.toFixed(2);
}

// ==========================================
// 10. Confirm Order / Place Order Action
// ==========================================
async function confirmOrder() {
    const session = getUserSession();
    if (!session.phone) {
        alert("Please log in to confirm your order.");
        return;
    }

    try {
        const res = await fetch(`/api/cart/${session.phone}`, {
            method: 'DELETE'
        });

        if (res.ok) {
            alert("🎉 Order placed successfully! Your chai & snacks are being prepared.");
            closeCartModal();
            fetchCartCount();
        } else {
            const data = await res.json();
            alert(data.error || "Failed to place order. Please try again.");
        }
    } catch (err) {
        console.error("Confirm Order Error:", err);
        alert("Network error. Could not place order.");
    }
}

// ==========================================
// 11. Modal Helper Functions
// ==========================================
function logoutUser() {
    localStorage.removeItem('cp_user_name');
    localStorage.removeItem('cp_user_phone');
    location.reload();
}

function openCartModal() {
    document.getElementById('cartModal').style.display = 'flex';
    fetchCartCount();
}

function closeCartModal() {
    document.getElementById('cartModal').style.display = 'none';
}

function openLoginModal() {
    clearAuthError(); // Clear any existing errors when opening modal
    document.getElementById('loginModal').style.display = 'flex';
    switchAuthTab('login'); // Default to Login tab on open
}

function closeLoginModal() {
    document.getElementById('loginModal').style.display = 'none';
    clearAuthError();
}