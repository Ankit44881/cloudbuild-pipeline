// 1. Session and Cart State Helper
function getUserSession() {
    return {
        name: localStorage.getItem('cp_user_name'),
        phone: localStorage.getItem('cp_user_phone')
    };
}

// 2. Page Load Initializer
document.addEventListener('DOMContentLoaded', () => {
    updateNavbarUI();
    fetchCartCount();
});

// 3. Navbar UI Sync Across Pages
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
                🔑 Login to Order
            </button>
        `;
    }
    navUl.appendChild(li);
}

// 4. Login Action
async function handleLogin(event) {
    event.preventDefault();
    const name = document.getElementById('loginName').value.trim();
    const phone = document.getElementById('loginPhone').value.trim();

    if (!name || !phone) {
        alert("Please enter Name and Phone number");
        return;
    }

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, phone })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('cp_user_name', data.name);
            localStorage.setItem('cp_user_phone', data.phone);
            closeLoginModal();
            updateNavbarUI();
            fetchCartCount();
        } else {
            alert(data.error || "Login failed");
        }
    } catch (err) {
        console.error("Login Error:", err);
    }
}

// 5. Add to Cart Logic (Used in menu.html)
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
                user_phone: session.phone,
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

// 6. Fetch Cart Details by User Phone Number
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

// 7. Render Modal Data
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
    document.getElementById('loginModal').style.display = 'flex';
}

function closeLoginModal() {
    document.getElementById('loginModal').style.display = 'none';
}