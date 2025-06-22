# Sample product database (would be replaced with actual database in production)
PRODUCT_DB = {
    "haircare": [
        {"id": "h1", "name": "Brazilian Hair Bundle", "price": 25000, "stock": 15},
        {"id": "h2", "name": "Peruvian Wig", "price": 35000, "stock": 8},
        {"id": "h3", "name": "Hair Growth Oil", "price": 5000, "stock": 0}
    ],
    "skincare": [
        {"id": "s1", "name": "Facial Cleanser", "price": 8500, "stock": 20},
        {"id": "s2", "name": "Vitamin C Serum", "price": 12000, "stock": 5},
        {"id": "s3", "name": "Moisturizer", "price": 7500, "stock": 0}
    ],
    "clothing": [
        {"id": "c1", "name": "Designer Jeans", "price": 15000, "stock": 10},
        {"id": "c2", "name": "Cotton T-shirt", "price": 5000, "stock": 25},
        {"id": "c3", "name": "Summer Dress", "price": 18000, "stock": 0}
    ]
}

# Sample orders database
ORDERS_DB = {
    "ORD123": {"status": "shipped", "tracking": "NGP78923X", "delivery_date": "May 20, 2025"},
    "ORD456": {"status": "processing", "tracking": None, "delivery_date": "May 25, 2025"},
    "ORD789": {"status": "delivered", "tracking": "NGP12345X", "delivery_date": "May 15, 2025"}
}

# Mock discount codes
DISCOUNT_CODES = {
    "WELCOME10": 0.10,
    "SUMMER25": 0.25,
    "SALE50": 0.50
}