# Mini Shop - Flask Edition

A lightweight, self-contained e-commerce application built with Flask that demonstrates server-side rendering and file-based data persistence.

## 📋 Project Overview

Mini Shop is a complete e-commerce solution built with Flask that fulfills all technical constraints:
- ✅ **Backend**: Flask with server-rendered pages (no APIs)
- ✅ **Storage**: JSON files (no database)
- ✅ **Frontend**: Plain HTML/CSS with minimal JavaScript
- ✅ **No external APIs** or SQL databases

## ✨ Features

### Customer Features
- **Product Catalog**: Browse all available products
- **Smart Filtering**: Search by name and filter by category
- **Shopping Cart**: Add/remove items and adjust quantities
- **Cart Persistence**: Cart maintained across sessions
- **Checkout Process**: Complete purchase with order confirmation
- **Order Summary**: View order details after purchase

### Admin Features
- **Admin Authentication**: Hardcoded login system
- **Product Management**: Add, edit, and view products
- **Inventory Control**: Update product stock and details
- **Activity Logging**: Audit trail of all important actions

### Technical Features
- **File-based Storage**: JSON files for products and orders
- **Audit Logging**: Comprehensive activity tracking
- **Session Management**: Cart persistence across requests
- **Form Validation**: Client and server-side validation

## 🚀 Quick Start

### Prerequisites
- Python 3.6+
- pip (Python package manager)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/sol654/Mini_Shop
   cd Mini-Shop
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

### Admin Access
- **URL**: `/admin/login`
- **Username**: `admin`
- **Password**: `12345`

## 📁 Project Structure

```
mini-shop/
├── app.py                 # Main Flask application
├── data/                  # Data storage directory
│   ├── products.json      # Product catalog
│   ├── orders.jsonl       # Order history (JSON Lines format)
│   └── audit.log          # System activity log
├── templates/             # HTML templates
│   ├── base.html          # Base template with navigation
│   ├── catalog.html       # Product listing page
│   ├── cart.html          # Shopping cart page
│   ├── checkout.html      # Checkout form
│   ├── order_summary.html # Order confirmation
│   ├── admin_login.html   # Admin authentication
│   └── admin_products.html # Product management
├── static/                # Static assets
│   ├── style.css          # Application styles
│   └── images/            # Product images
└── README.md              # This file
```

## 🔧 Technical Implementation

### Data Storage
- **Products**: JSON file with array of product objects
- **Orders**: JSONL (JSON Lines) format for append-only order history
- **Logs**: Plain text audit log with timestamped events

### Key Functions
- `load_products()`: Reads product data from JSON file
- `save_products()`: Writes product data to JSON file
- `append_order()`: Appends new orders to JSONL file
- `log_event()`: Records activities to audit log

### Routes Overview
| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Product catalog with search/filter |
| `/cart/add` | POST | Add item to shopping cart |
| `/cart` | GET | View shopping cart |
| `/cart/update` | POST | Update cart quantities |
| `/checkout` | GET, POST | Checkout process |
| `/order/<order_id>` | GET | Order confirmation |
| `/admin/login` | GET, POST | Admin authentication |
| `/admin/products` | GET | Product management |
| `/admin/products/update` | POST | Add/update products |
| `/admin/logout` | GET | Admin logout |

## 🛒 Using the Application

### Browsing Products
1. Visit the homepage to see all products
2. Use the search box to find specific items
3. Filter by category using the dropdown
4. Click "Add to Cart" to purchase items

### Managing Cart
1. View your cart by clicking "Cart" in the navigation
2. Adjust quantities using the number inputs
3. Remove items by setting quantity to zero
4. Proceed to checkout when ready

### Admin Tasks
1. Log in with admin credentials
2. Add new products using the form
3. Edit existing products by updating fields
4. All changes are persisted to the JSON file

## 📊 Data Models

### Product Schema
```json
{
  "id": "P-001",
  "name": "USB Keyboard",
  "price": 799,
  "stock": 12,
  "category": "Peripherals",
  "image": "/static/keyboard.jpg"
}
```

### Order Schema
```json
{
  "id": "ABC123",
  "customer": {
    "name": "John Doe",
    "email": "solace@example.com",
    "address": "123 Main St"
  },
  "items": [
    {
      "product_id": "P-001",
      "name": "USB Keyboard",
      "price": 799,
      "quantity": 1,
      "total": 799
    }
  ],
  "total": 799,
  "date": "2023-11-15T10:30:00.000Z"
}
```

## 🔍 Audit Logging

The application maintains a comprehensive audit log (`data/audit.log`) that records:
- User login attempts (successful and failed)
- Add to cart actions
- Checkout completions
- Product changes (additions and updates)
- Admin logouts

Example log entry:
```
2023-11-15 10:30:45 - ADD_TO_CART - Product: USB Keyboard, Qty: 1
```

## 🎨 Styling

The application uses custom CSS with:
- Responsive design for mobile and desktop
- Clean, modern interface
- Consistent color scheme and typography
- Intuitive navigation and forms

## 🔮 Future Enhancements

Potential improvements for the application:
- User registration and profiles
- Order history for customers
- Product images and galleries
- Inventory management alerts
- Enhanced search with filters
- Order status tracking

## 📝 License

This project is created for educational purposes as part of a backend development exercise.

## 🤝 Contributing

As this is a demonstration project following specific technical constraints, contributions should maintain the core requirements:
- No database systems
- No external APIs
- Server-rendered pages only
- File-based storage

---

