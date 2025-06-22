from typing import Dict, Any, Optional
from langchain_core.tools import tool

#from Zita.app import business_type
from .product_tools import check_product_availability



@tool
def handle_negotiation(product_name: str, offered_price: float, max_price: Optional[float] = None, min_price: Optional[float] = None) -> Dict[str, Any]:
    """Handle price negotiations for products"""
    product_info = check_product_availability(product_name)
    
    if not product_info["found"]:
        return {
            "success": False,
            "message": product_info["message"]
        }
    
    if not product_info["available"]:
        return {
            "success": False,
            "message": f"Sorry, {product_info['product']} is currently out of stock. Would you like to see some alternatives?"
        }
    
    original_price = product_info["price"]
    max_price = max_price if max_price is not None else original_price
    default_min_price = original_price * 0.8
    min_price = min_price if min_price is not None else default_min_price
    min_price = min(min_price, max_price)
    
    discount_percentage = ((original_price - offered_price) / original_price) * 100
    
    # Prepare negotiation context for LLM
    negotiation_prompt = f"""
        You are Zita, a sharp Nigerian seller that can switch between pidgin and Nigerian English based on user input, help negotiate the price for {product_info['product']} in a way that's both friendly and persuasive.

        Product info:
        - Original price: ₦{original_price:,}
        - Customer's offer: ₦{offered_price:,}
        - Minimum acceptable price: ₦{min_price:,}
        - Maximum price: ₦{max_price:,}
        - Discount percentage: {discount_percentage:.1f}%

        Your negotiation style:
        - Be street-smart, witty, and warm — like a trusted vendor at a Lagos market or popular online store.
        - If chatting in Pidgin, feel free to sprinkle in common phrases like *"abeg"*, *"no vex"*, *"e go better for you"*, *"na last price be this o"*, etc.
        - If in English, sound friendly and playful but professional — never too stiff.

        Negotiation logic (but don’t reveal it directly):
        1. If offer ≥ max_price:
        - Accept quickly and thank the customer warmly. Maybe say “You sabi better thing!” or “Nice one! You go enjoy am.”
        2. If min_price ≤ offer < max_price:
        - Accept or make a soft counter-offer. Say something like: “Ah, you sharp, but top ₦500 go make sense for me abeg.”
        3. If offer < min_price:
        - Decline sweetly but push your lowest. Use charm: “Chai! I for love run you am, but the price na blood. ₦{min_price:,} na my last — no shaking.”

        Additional tips:
        - Suggest bundles, delivery, or small bonus if it helps close the deal.
        - Make customer feel smart, appreciated, and like they’re winning — even when you push back.

        DO NOT mention pricing logic or thresholds explicitly. Keep your tone human and real. The goal is to close the deal like a Naija seller who knows how to read people.

        Example response:
        "Ah oga, your offer dey nice o, but make I talk true — ₦{min_price:,} na the very bottom. Na correct item be this, you no go regret am. I fit add small delivery bonus for you too, how you see am?"
    """

    
    # Get LLM response for negotiation
    response_text, _, _ = get_response(negotiation_prompt, api_key, "e-commerce")
    
    # Determine negotiation outcome
    if offered_price >= max_price:
        final_price = max_price
        success = True
    elif offered_price >= min_price:
        # If offer is close to min price (in the bottom 20% of range), accept it
        price_range = max_price - min_price
        offer_position = (offered_price - min_price) / price_range if price_range > 0 else 1
        if offer_position >= 0.8:
            final_price = offered_price
            success = True
        else:
            counter_position = 0.7 - (offer_position * 0.5)
            counter_position = max(0.1, min(counter_position, 0.9))
            final_price = min_price + (price_range * counter_position)
            success = True
    else:
        success = False
        final_price = None
    
    result = {
        "success": success,
        "product": product_info["product"],
        "original_price": original_price,
        "max_price": max_price,
        "min_price": min_price,
        "offered_price": offered_price,
        "message": response_text
    }
    
    if final_price is not None:
        result["final_price"] = final_price
        if final_price != offered_price:
            result["counter_offer"] = final_price
    
    if success and final_price == offered_price:
        result["discount_percentage"] = discount_percentage
    
    return result











# @tool
# def handle_negotiation(product_name: str, offered_price: float, max_price: Optional[float] = None, min_price: Optional[float] = None) -> Dict[str, Any]:
#     """Handle price negotiations for products"""
#     product_info = check_product_availability(product_name)
    
#     if not product_info["found"]:
#         return {
#             "success": False,
#             "message": product_info["message"]
#         }
    
#     if not product_info["available"]:
#         return {
#             "success": False,
#             "message": f"Sorry, {product_info['product']} is currently out of stock. Would you like to see some alternatives?"
#         }
    
#     original_price = product_info["price"]
    
#     # Use provided max_price or default to original price
#     max_price = max_price if max_price is not None else original_price
    
#     # Use provided min_price or default to 80% of original price
#     default_min_price = original_price * 0.8
#     min_price = min_price if min_price is not None else default_min_price
    
#     # Ensure min_price doesn't exceed max_price
#     min_price = min(min_price, max_price)
    
#     # Calculate discount percentage
#     discount_percentage = ((original_price - offered_price) / original_price) * 100
    
#     if offered_price >= max_price:
#         # Customer offered full price or more than our max price
#         return {
#             "success": True,
#             "product": product_info["product"],
#             "original_price": original_price,
#             "max_price": max_price,
#             "offered_price": offered_price,
#             "final_price": max_price,
#             "message": f"Thank you for your interest in {product_info['product']}! We can accept your offer of ₦{max_price:,}."
#         }
#     elif offered_price >= min_price:
#         # Offer is within negotiable range
#         # Calculate a counter-offer between min_price and max_price
#         # The closer to min_price, the closer to accepting
#         price_range = max_price - min_price
#         offer_position = (offered_price - min_price) / price_range if price_range > 0 else 1
        
#         # If offer is close to min price (in the bottom 20% of range), accept it
#         if offer_position >= 0.8:
#             final_price = offered_price
#             return {
#                 "success": True,
#                 "product": product_info["product"],
#                 "original_price": original_price,
#                 "max_price": max_price,
#                 "min_price": min_price,
#                 "offered_price": offered_price,
#                 "final_price": final_price,
#                 "discount_percentage": discount_percentage,
#                 "message": f"Great news! We can accept your offer of ₦{offered_price:,} for the {product_info['product']}. That's a {discount_percentage:.1f}% discount!"
#             }
#         else:
#             # Counter-offer based on position in the negotiation range
#             # The lower the offer, the closer the counter-offer to min_price
#             counter_position = 0.7 - (offer_position * 0.5)  # Adjust this formula as needed
#             counter_position = max(0.1, min(counter_position, 0.9))  # Keep between 10% and 90%
#             counter_offer = min_price + (price_range * counter_position)
            
#             return {
#                 "success": True,
#                 "product": product_info["product"],
#                 "original_price": original_price,
#                 "max_price": max_price,
#                 "min_price": min_price,
#                 "offered_price": offered_price,
#                 "counter_offer": counter_offer,
#                 "message": f"Thank you for your offer of ₦{offered_price:,} for the {product_info['product']}. The best we can do is ₦{counter_offer:,}. Would that work for you?"
#             }
#     else:
#         # Offer is too low (below min_price)
#         return {
#             "success": False,
#             "product": product_info["product"],
#             "original_price": original_price,
#             "max_price": max_price,
#             "min_price": min_price,
#             "offered_price": offered_price,
#             "message": f"Thank you for your interest in {product_info['product']}. Your offer of ₦{offered_price:,} is below what we can accept. The current price is ₦{original_price:,}, but we could consider an offer of at least ₦{min_price:,}. Would you like to make another offer?"
#         }