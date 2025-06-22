from typing import Dict, List, Any, Optional
from langchain_core.tools import tool
from data.mock_data import PRODUCT_DB

@tool
def enhance_product_search_with_llm(product_query: str, category: Optional[str] = None) -> Dict[str, Any]:
    """Use LLM to find the best matching product for a natural language query"""
    from Zita.data.mock_data import PRODUCT_DB
    
    # Prepare the prompt for the LLM
    prompt = f"Given the product query: '{product_query}', find the best matching products from the following categories and items:\n\n"
    
    # Add category-specific context if provided
    if category and category in PRODUCT_DB:
        products = PRODUCT_DB[category]
        prompt += f"Category: {category}\nProducts: {products}\n"
    else:
        # Include all categories
        prompt += "Available categories and products:\n"
        for cat, products in PRODUCT_DB.items():
            prompt += f"\n{cat.capitalize()}:\n"
            for product in products:
                prompt += f"- {product['name']} (${product['price']/100:.2f})\n"
    
    prompt += "\nPlease analyze the query and return:\n"
    prompt += "1. The best matching products\n"
    prompt += "2. Why these products match the query\n"
    prompt += "3. Any alternative suggestions\n"
    
    try:
        # Send prompt to LLM (replace with your actual LLM call)
        # For example: response = llm.generate(prompt)
        
        # Process LLM response and find matching products
        matches = []
        for cat, products in PRODUCT_DB.items():
            if category and category != cat:
                continue
            
            for product in products:
                # Here you would use the LLM's response to determine matches
                # For now, we'll do a simple text matching
                if any(word.lower() in product['name'].lower() for word in product_query.split()):
                    matches.append({
                        "category": cat,
                        "product": product,
                        "relevance_score": 0.8,  # This would come from LLM
                        "reason": f"Product name matches query terms",  # This would come from LLM
                    })
        
        if matches:
            return {
                "found": True,
                "matches": matches,
                "alternatives": [p for p in matches[1:] if p["relevance_score"] > 0.5],
                "query_understanding": "Product search based on name matching"  # This would come from LLM
            }
        
        return {
            "found": False,
            "suggestion": "No matching products found. Consider browsing our categories: " + 
                         ", ".join(PRODUCT_DB.keys())
        }
        
    except Exception as e:
        return {
            "found": False,
            "error": str(e),
            "suggestion": "An error occurred while processing your request. Please try again."
        }

@tool
def check_product_availability(product_name: str, category: Optional[str] = None) -> Dict[str, Any]:
    """Check if a product is available and return its details"""
    product_name = product_name.lower()
    
    # Use LLM to enhance search capabilities
    # This could be a separate function call to your LLM
    enhanced_search_results = enhance_product_search_with_llm(product_name, category)
    
    # If LLM found a good match, return it
    if enhanced_search_results.get("found"):
        return enhanced_search_results
    
    # Fallback to traditional search if LLM doesn't find a match
    # Search in specific category if provided
    if category and category.lower() in PRODUCT_DB:
        categories = [category.lower()]
    else:
        categories = PRODUCT_DB.keys()
    
    for cat in categories:
        for product in PRODUCT_DB[cat]:
            if product_name in product["name"].lower():
                available = product["stock"] > 0
                return {
                    "found": True,
                    "product": product["name"],
                    "price": product["price"],
                    "available": available,
                    "stock": product["stock"],
                    "message": f"Found {product['name']} - ₦{product['price']:,}. {'In stock' if available else 'Out of stock'}"
                }
    
    return {
        "found": False,
        "message": f"Sorry, I couldn't find {product_name} in our inventory."
    }


@tool
def recommend_alternatives(product_name: str) -> Dict[str, Any]:
    """Recommend alternative products when a requested item is out of stock"""
    # First check if the product exists
    product_info = check_product_availability(product_name)
    
    # Extract keywords from the product name
    keywords = product_name.lower().split()
    
    # Find potential category based on keywords
    potential_category = None
    for category in PRODUCT_DB.keys():
        if any(keyword in category.lower() for keyword in keywords):
            potential_category = category
            break
    
    # If we found an exact match but it's out of stock, use its category
    if product_info.get("found", False):
        # If product exists and is in stock, no need for alternatives
        if product_info.get("available", False):
            return {
                "success": False,
                "message": f"{product_info['product']} is available in stock, no alternatives needed."
            }
        
        # Find the category the product belongs to
        for category, products in PRODUCT_DB.items():
            for product in products:
                if product_name.lower() in product["name"].lower():
                    potential_category = category
                    break
            if potential_category:
                break
    
    # If we still don't have a category, try to find the most relevant one
    if not potential_category:
        # Count matches in each category
        category_matches = {}
        for category, products in PRODUCT_DB.items():
            matches = 0
            for product in products:
                product_lower = product["name"].lower()
                for keyword in keywords:
                    if keyword in product_lower:
                        matches += 1
            if matches > 0:
                category_matches[category] = matches
        
        # Get the category with the most matches
        if category_matches:
            potential_category = max(category_matches.items(), key=lambda x: x[1])[0]
        else:
            # If no matches, just pick the first category as a fallback
            potential_category = list(PRODUCT_DB.keys())[0]
    
    # Find alternatives in the potential category
    alternatives = []
    if potential_category:
        for product in PRODUCT_DB[potential_category]:
            # Only include products that are in stock
            if product["stock"] > 0:
                # If we found an exact match, don't include it in alternatives
                if product_info.get("found", False) and product_name.lower() in product["name"].lower():
                    continue
                alternatives.append({
                    "name": product["name"],
                    "price": product["price"],
                    "stock": product["stock"]
                })
    
    if alternatives:
        alternatives_text = ", ".join([f"{alt['name']} (₦{alt['price']:,})" for alt in alternatives])
        if product_info.get("found", False):
            return {
                "success": True,
                "product": product_info["product"],
                "alternatives": alternatives,
                "message": f"{product_info['product']} is out of stock. Here are some alternatives: {alternatives_text}."
            }
        else:
            return {
                "success": True,
                "product": product_name,
                "alternatives": alternatives,
                "message": f"We couldn't find '{product_name}' in our inventory. Here are some similar products you might like: {alternatives_text}."
            }
    
    return {
        "success": False,
        "message": f"Sorry, we couldn't find '{product_name}' or any suitable alternatives in our inventory."
    }

@tool
def apply_discount(product_name: str, discount_code: str) -> Dict[str, Any]:
    """Apply a discount code to a product"""
    from data.mock_data import DISCOUNT_CODES
    
    product_info = check_product_availability(product_name)
    
    if not product_info["found"]:
        return {
            "success": False,
            "message": product_info["message"]
        }
    
    if discount_code.upper() in DISCOUNT_CODES:
        discount_rate = DISCOUNT_CODES[discount_code.upper()]
        original_price = product_info["price"]
        discounted_price = original_price * (1 - discount_rate)
        
        return {
            "success": True,
            "product": product_info["product"],
            "original_price": original_price,
            "discount_rate": discount_rate * 100,
            "discounted_price": discounted_price,
            "message": f"Discount code {discount_code} applied! {product_info['product']} price reduced from ₦{original_price:,} to ₦{discounted_price:,}."
        }
    
    return {
        "success": False,
        "message": f"Sorry, the discount code {discount_code} is invalid or expired."
    }