import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = '83328af063c5d7994d0fdb5147e71509926aaf1fbedcd558'

# File paths
DATA_DIR = 'data'
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.json')
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.jsonl')
AUDIT_LOG = os.path.join(DATA_DIR, 'audit.log')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Hardcoded admin credentials
ADMIN_CREDENTIALS = {"username": "admin", "password": "12345"}

# Helper functions
def load_products():
    """Load products from JSON file with comprehensive error handling"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Create default products if file doesn't exist
        if not os.path.exists(PRODUCTS_FILE):
            initial_products = [
                {"id": "P-001", "name": "USB Keyboard", "price": 799, "stock": 12, 
                 "category": "Peripherals", "image": "/static/images/keyboard.jpg"},
                {"id": "P-002", "name": "USB Mouse", "price": 399, "stock": 20, 
                 "category": "Peripherals", "image": "/static/images/mouse.jpg"},
                {"id": "P-003", "name": "HDMI Cable", "price": 199, "stock": 30, 
                 "category": "Cables", "image": "/static/images/hdmi.jpg"}
            ]
            save_products(initial_products)
            return initial_products
        
        # Load existing products
        with open(PRODUCTS_FILE, 'r') as f:
            products = json.load(f)
            
        return products
        
    except json.JSONDecodeError:
        print("Error: products.json contains invalid JSON")
        return []
    except Exception as e:
        print(f"Error loading products: {e}")
        return []

def save_products(products):
    """Save products to JSON file"""
    try:
        with open(PRODUCTS_FILE, 'w') as f:
            json.dump(products, f, indent=2)
    except Exception as e:
        print(f"Error saving products: {e}")

def append_order(order):
    """Append order to JSONL file"""
    try:
        with open(ORDERS_FILE, 'a') as f:
            f.write(json.dumps(order) + '\n')
    except Exception as e:
        print(f"Error appending order: {e}")

def log_event(event_type, details):
    """Log events to audit log"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - {event_type} - {details}\n"
        with open(AUDIT_LOG, 'a') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error logging event: {e}")

@app.before_request
def before_request():
    """Initialize cart before each request"""
    try:
        if 'cart' not in session:
            session['cart'] = {}
    except Exception as e:
        print(f"Error in before_request: {e}")
        session['cart'] = {}

# Routes
@app.route('/')
def catalog():
    """Show product catalog with optional search and filtering"""
    try:
        products = load_products()
        
        # Handle search
        search_query = request.args.get('q', '')
        if search_query:
            products = [p for p in products if search_query.lower() in p['name'].lower()]
        
        # Handle category filter
        category_filter = request.args.get('category', '')
        if category_filter:
            products = [p for p in products if p['category'] == category_filter]
        
        # Get unique categories for filter dropdown
        all_products = load_products()
        categories = []
        try:
            categories = list(set(p['category'] for p in all_products if 'category' in p))
        except:
            categories = ['Peripherals', 'Cables', 'Audio']
        
        # Calculate cart total for display in navbar
        cart_total = sum(session['cart'].values()) if 'cart' in session else 0
        
        return render_template('catalog.html', 
                             products=products, 
                             categories=categories,
                             search_query=search_query,
                             cart_total=cart_total)
                             
    except Exception as e:
        print(f"Error in catalog: {e}")
        return render_template('catalog.html', 
                             products=[], 
                             categories=[],
                             search_query='',
                             cart_total=0)

@app.route('/cart/add', methods=['POST'])
def cart_add():
    """Add product to cart"""
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('qty', 1))
        
        if product_id and quantity > 0:
            # Update cart quantity
            session['cart'][product_id] = session['cart'].get(product_id, 0) + quantity
            session.modified = True
            
            # Log the event
            products = load_products()
            product_name = next((p['name'] for p in products if p['id'] == product_id), 'Unknown Product')
            log_event('ADD_TO_CART', f"Product: {product_name}, Qty: {quantity}")
            
            flash(f'Added {quantity} x {product_name} to cart', 'success')
        
        return redirect(url_for('catalog'))
    
    except Exception as e:
        print(f"Error in cart_add: {e}")
        flash('Error adding item to cart', 'error')
        return redirect(url_for('catalog'))

@app.route('/cart')
def view_cart():
    """View shopping cart"""
    try:
        cart_items = []
        total = 0
        products = load_products()
        
        for product_id, quantity in session.get('cart', {}).items():
            product = next((p for p in products if p['id'] == product_id), None)
            if product:
                # Ensure image path is correctly formatted
                if 'image' not in product or not product['image']:
                    product['image'] = '/static/images/placeholder.jpg'
                elif not product['image'].startswith('/static/'):
                    product['image'] = '/static/images/' + product['image']
                
                item_total = product['price'] * quantity
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total': item_total
                })
                total += item_total
        
        cart_total = sum(session.get('cart', {}).values())
        return render_template('cart.html', 
                             cart_items=cart_items, 
                             total=total,
                             cart_total=cart_total)
    
    except Exception as e:
        print(f"Error in view_cart: {e}")
        return render_template('cart.html', 
                             cart_items=[], 
                             total=0,
                             cart_total=0)

@app.route('/cart/update', methods=['POST'])
def update_cart():
    """Update cart quantities"""
    try:
        products = load_products()
        cart = session.get('cart', {})
        
        for product in products:
            product_id = product['id']
            if product_id in cart:
                new_qty = int(request.form.get(f'qty_{product_id}', 0))
                
                if new_qty <= 0:
                    # Remove item if quantity is 0 or less
                    product_name = product['name']
                    cart.pop(product_id)
                    flash(f'Removed {product_name} from cart', 'info')
                else:
                    # Update quantity
                    cart[product_id] = new_qty
        
        session['cart'] = cart
        session.modified = True
        return redirect(url_for('view_cart'))
    
    except Exception as e:
        print(f"Error in update_cart: {e}")
        flash('Error updating cart', 'error')
        return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout process"""
    try:
        if not session.get('cart'):
            flash('Your cart is empty', 'warning')
            return redirect(url_for('catalog'))
        
        if request.method == 'POST':
            # Validate form data
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            address = request.form.get('address', '').strip()
            
            if not name or not email or not address:
                flash('Please fill all required fields', 'error')
                return render_template('checkout.html', cart_total=sum(session.get('cart', {}).values()))
            
            # Validate cart quantities against stock
            products = load_products()
            cart = session.get('cart', {})
            
            for product_id, quantity in cart.items():
                product = next((p for p in products if p['id'] == product_id), None)
                if not product or product['stock'] < quantity:
                    flash(f'Not enough stock for {product["name"] if product else "unknown product"}', 'error')
                    return redirect(url_for('view_cart'))
            
            # Create order
            order_id = str(uuid.uuid4())[:8].upper()
            order_items = []
            order_total = 0
            
            for product_id, quantity in cart.items():
                product = next((p for p in products if p['id'] == product_id))
                item_total = product['price'] * quantity
                order_items.append({
                    'product_id': product_id,
                    'name': product['name'],
                    'price': product['price'],
                    'quantity': quantity,
                    'total': item_total
                })
                order_total += item_total
                
                # Reduce stock
                product['stock'] -= quantity
            
            # Save updated products
            save_products(products)
            
            # Create order record
            order = {
                'id': order_id,
                'customer': {
                    'name': name,
                    'email': email,
                    'address': address
                },
                'items': order_items,
                'total': order_total,
                'date': datetime.now().isoformat()
            }
            
            # Save order
            append_order(order)
            
            # Log the event
            log_event('CHECKOUT', f"Order: {order_id}, Total: ${order_total/100:.2f}")
            
            # Clear cart
            session['cart'] = {}
            session.modified = True
            
            return redirect(url_for('order_summary', order_id=order_id))
        
        cart_total = sum(session.get('cart', {}).values())
        return render_template('checkout.html', cart_total=cart_total)
    
    except Exception as e:
        print(f"Error in checkout: {e}")
        flash('Error during checkout', 'error')
        return redirect(url_for('view_cart'))

@app.route('/order/<order_id>')
def order_summary(order_id):
    """Show order summary"""
    try:
        cart_total = sum(session.get('cart', {}).values())
        return render_template('order_summary.html', order_id=order_id, cart_total=cart_total)
    except Exception as e:
        print(f"Error in order_summary: {e}")
        return render_template('order_summary.html', order_id='ERROR', cart_total=0)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            if username == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']:
                session['is_admin'] = True
                log_event('ADMIN_LOGIN', 'Success')
                flash('Login successful', 'success')
                return redirect(url_for('admin_products'))
            else:
                log_event('ADMIN_LOGIN', 'Failed attempt')
                flash('Invalid credentials', 'error')
        
        cart_total = sum(session.get('cart', {}).values())
        return render_template('admin_login.html', cart_total=cart_total)
    
    except Exception as e:
        print(f"Error in admin_login: {e}")
        return render_template('admin_login.html', cart_total=0)

@app.route('/admin/products')
def admin_products():
    """Admin product management"""
    try:
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        
        products = load_products()
        cart_total = sum(session.get('cart', {}).values())
        return render_template('admin_products.html', products=products, cart_total=cart_total)
    
    except Exception as e:
        print(f"Error in admin_products: {e}")
        return redirect(url_for('admin_login'))

@app.route('/admin/products/update', methods=['POST'])
def admin_update_products():
    """Add or update products"""
    try:
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        
        products = load_products()
        product_id = request.form.get('id')
        
        if product_id:  # Update existing product
            product = next((p for p in products if p['id'] == product_id), None)
            if product:
                product['name'] = request.form.get('name')
                product['price'] = int(request.form.get('price'))
                product['stock'] = int(request.form.get('stock'))
                product['category'] = request.form.get('category')
                product['image'] = request.form.get('image')
                log_event('PRODUCT_UPDATE', f"Product: {product['name']}")
        else:  # Add new product
            new_product = {
                'id': f"P-{str(len(products) + 1).zfill(3)}",
                'name': request.form.get('name'),
                'price': int(request.form.get('price')),
                'stock': int(request.form.get('stock')),
                'category': request.form.get('category'),
                'image': request.form.get('image')
            }
            products.append(new_product)
            log_event('PRODUCT_ADD', f"Product: {new_product['name']}")
        
        save_products(products)
        flash('Product saved successfully', 'success')
        return redirect(url_for('admin_products'))
    
    except Exception as e:
        print(f"Error in admin_update_products: {e}")
        flash('Error saving product', 'error')
        return redirect(url_for('admin_products'))

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    try:
        session.pop('is_admin', None)
        log_event('ADMIN_LOGOUT', 'Success')
        flash('Logged out successfully', 'info')
        return redirect(url_for('catalog'))
    except Exception as e:
        print(f"Error in admin_logout: {e}")
        return redirect(url_for('catalog'))

if __name__ == '__main__':
    app.run()
