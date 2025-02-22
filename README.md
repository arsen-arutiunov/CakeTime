# 📌 Cake Time API Documentation


## 🏷️ Authentication & User Management

### **1. Register a New User**  
**Endpoint:** `POST /api/register/`

**Description:** Creates a new user account.

📥 **Request Body**
```json
{
    "email": "user@example.com",
    "username": "newuser",
    "password": "securepassword"
}
```

✅ **Response (201 Created)**
```json
{
    "id": 1,
    "username": "newuser",
    "email": "user@example.com"
}
```

---

### **2. User Login**  
**Endpoint:** `POST /api/login/`

**Description:** Authenticates a user and returns JWT tokens.

📥 **Request Body**
```json
{
    "email": "user@example.com",
    "password": "securepassword"
}
```

✅ **Response (200 OK)**
```json
{
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token"
}
```

---

### **3. Get User Profile**  
**Endpoint:** `GET /api/profile/`  
**Description:** Returns the authenticated user's profile information.

✅ **Response (200 OK)**
```json
{
    "id": 1,
    "username": "newuser",
    "email": "user@example.com"
}
```

---

### **4. Update User Profile**  
**Endpoint:** `PUT /api/profile/`  
**Description:** Updates the authenticated user's profile.

📥 **Request Body**
```json
{
    "username": "updateduser"
}
```

✅ **Response (200 OK)**
```json
{
    "id": 1,
    "username": "updateduser",
    "email": "user@example.com"
}
```

---

# 📦 Products API Documentation  

## 🏷️ Categories

### **1. Get All Categories**  
**Endpoint:** `GET /api/categories/`  
**Description:** Returns a list of all available categories.

✅ **Response (200 OK)**
```json
[
    {
        "id": 1,
        "name": "Cakes"
    },
    {
        "id": 2,
        "name": "Macarons"
    }
]
```

### **2. Get Category by ID**  
**Endpoint:** `GET /api/categories/{id}/`  
**Description:** Returns details of a specific category by ID.

✅ **Response (200 OK)**
```json
{
    "id": 1,
    "name": "Cakes"
}
```

### **3. Create a New Category**  
**Endpoint:** `POST /api/categories/`  
**Description:** Creates a new category.

📥 **Request Body**
```json
{
    "name": "Pies"
}
```

✅ **Response (201 Created)**
```json
{
    "id": 3,
    "name": "Pies"
}
```

### **4. Update a Category**  
**Endpoint:** `PUT /api/categories/{id}/`  
**Description:** Updates an existing category.

📥 **Request Body**
```json
{
    "name": "Updated Cakes"
}
```

✅ **Response (200 OK)**
```json
{
    "id": 1,
    "name": "Updated Cakes"
}
```

### **5. Delete a Category**  
**Endpoint:** `DELETE /api/categories/{id}/`  
**Description:** Deletes a category.

✅ **Response (204 No Content)**

---

## 🏷️ Products

### **1. Get All Products**  
**Endpoint:** `GET /api/products/`  
**Description:** Returns a list of all available products.

✅ **Response (200 OK)**
```json
[
    {
        "id": 1,
        "name": "Chocolate Cake",
        "description": "Delicious chocolate cake",
        "price": "25.99",
        "image": "/media/products/chocolate_cake.jpg",
        "category": {
            "id": 1,
            "name": "Cakes"
        }
    }
]
```

### **2. Get Product by ID**  
**Endpoint:** `GET /api/products/{id}/`  
**Description:** Returns details of a specific product by ID.

✅ **Response (200 OK)**
```json
{
    "id": 1,
    "name": "Chocolate Cake",
    "description": "Delicious chocolate cake",
    "price": "25.99",
    "image": "/media/products/chocolate_cake.jpg",
    "category": {
        "id": 1,
        "name": "Cakes"
    }
}
```

### **3. Create a New Product**  
**Endpoint:** `POST /api/products/`  
**Description:** Creates a new product.

📥 **Request Body**
```json
{
    "name": "Vanilla Cake",
    "description": "Soft and creamy vanilla cake",
    "price": "20.50",
    "image": "/media/products/vanilla_cake.jpg",
    "category": 1
}
```

✅ **Response (201 Created)**
```json
{
    "id": 2,
    "name": "Vanilla Cake",
    "description": "Soft and creamy vanilla cake",
    "price": "20.50",
    "image": "/media/products/vanilla_cake.jpg",
    "category": {
        "id": 1,
        "name": "Cakes"
    }
}
```

### **4. Update a Product**  
**Endpoint:** `PUT /api/products/{id}/`  
**Description:** Updates an existing product.

📥 **Request Body**
```json
{
    "name": "Updated Vanilla Cake",
    "description": "New and improved recipe",
    "price": "22.00",
    "category": 1
}
```

✅ **Response (200 OK)**
```json
{
    "id": 2,
    "name": "Updated Vanilla Cake",
    "description": "New and improved recipe",
    "price": "22.00",
    "category": {
        "id": 1,
        "name": "Cakes"
    }
}
```

### **5. Delete a Product**  
**Endpoint:** `DELETE /api/products/{id}/`  
**Description:** Deletes a product.

✅ **Response (204 No Content)**

---

## 🏷️ Cart Management

### **1. View Cart**  
**Endpoint:** `GET /api/cart/`  
**Description:** Returns the current user's cart with items and total price.

✅ **Response (200 OK)**
```json
{
    "id": 1,
    "items": [
        {
            "product": {
                "id": 1,
                "name": "Chocolate Cake",
                "price": "25.99"
            },
            "quantity": 2,
            "total_price": "51.98"
        }
    ],
    "total": "51.98"
}
```

---

### **2. Add Item to Cart**  
**Endpoint:** `POST /api/cart/add/`  
**Description:** Adds a product to the user's cart or updates the quantity if the product already exists.

📥 **Request Body**
```json
{
    "product_id": 1,
    "quantity": 2
}
```

✅ **Response (200 OK)**
```json
{
    "message": "Product added to cart",
    "cart": {
        "id": 1,
        "items": [
            {
                "product": {
                    "id": 1,
                    "name": "Chocolate Cake",
                    "price": "25.99"
                },
                "quantity": 2,
                "total_price": "51.98"
            }
        ],
        "total": "51.98"
    }
}
```

---

### **3. Update Cart Item**  
**Endpoint:** `PUT /api/cart/update/{id}/`  
**Description:** Updates the quantity of a specific cart item.

📥 **Request Body**
```json
{
    "quantity": 3
}
```

✅ **Response (200 OK)**
```json
{
    "message": "Cart updated successfully",
    "cart": {
        "id": 1,
        "items": [
            {
                "product": {
                    "id": 1,
                    "name": "Chocolate Cake",
                    "price": "25.99"
                },
                "quantity": 3,
                "total_price": "77.97"
            }
        ],
        "total": "77.97"
    }
}
```

---

### **4. Remove Item from Cart**  
**Endpoint:** `DELETE /api/cart/remove/{id}/`  
**Description:** Removes a product from the user's cart.

✅ **Response (200 OK)**
```json
{
    "message": "Product removed from cart",
    "cart": {
        "id": 1,
        "items": [],
        "total": "0.00"
    }
}
```

---

### **5. Clear Cart**  
**Endpoint:** `DELETE /api/cart/clear/`  
**Description:** Removes all items from the user's cart.

✅ **Response (200 OK)**
```json
{
    "message": "Cart cleared successfully",
    "cart": {
        "id": 1,
        "items": [],
        "total": "0.00"
    }
}
```
---

## 🏷️ Orders Management

### **1. Get All Orders**  
**Endpoint:** `GET /api/orders/`  
**Description:** Returns a list of all orders for the authenticated user.

✅ **Response (200 OK)**
```json
[
    {
        "id": 1,
        "user": {
            "id": 2,
            "username": "johndoe"
        },
        "items": [
            {
                "product": {
                    "id": 1,
                    "name": "Chocolate Cake",
                    "price": "25.99"
                },
                "quantity": 2,
                "total_price": "51.98"
            }
        ],
        "total": "51.98",
        "status": "Pending"
    }
]
```

---

### **2. Get Order by ID**  
**Endpoint:** `GET /api/orders/{id}/`  
**Description:** Returns details of a specific order by ID.

✅ **Response (200 OK)**
```json
{
    "id": 1,
    "user": {
        "id": 2,
        "username": "johndoe"
    },
    "items": [
        {
            "product": {
                "id": 1,
                "name": "Chocolate Cake",
                "price": "25.99"
            },
            "quantity": 2,
            "total_price": "51.98"
        }
    ],
    "total": "51.98",
    "status": "Pending"
}
```

---

### **3. Create a New Order**  
**Endpoint:** `POST /api/orders/`  
**Description:** Creates a new order for the authenticated user.

📥 **Request Body**
```json
{
    "items": [
        {
            "product_id": 1,
            "quantity": 2
        }
    ]
}
```

✅ **Response (201 Created)**
```json
{
    "id": 2,
    "user": {
        "id": 2,
        "username": "johndoe"
    },
    "items": [
        {
            "product": {
                "id": 1,
                "name": "Chocolate Cake",
                "price": "25.99"
            },
            "quantity": 2,
            "total_price": "51.98"
        }
    ],
    "total": "51.98",
    "status": "Pending"
}
```

---

### **4. Update Order Status**  
**Endpoint:** `PUT /api/orders/{id}/`  
**Description:** Updates the status of an order (admin only).

📥 **Request Body**
```json
{
    "status": "Shipped"
}
```

✅ **Response (200 OK)**
```json
{
    "id": 1,
    "status": "Shipped"
}
```

---

### **5. Cancel an Order**  
**Endpoint:** `DELETE /api/orders/{id}/`  
**Description:** Cancels an order (only allowed if it's still pending).

✅ **Response (200 OK)**
```json
{
    "message": "Order canceled successfully"
}
```

