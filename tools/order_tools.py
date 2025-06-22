from typing import Dict, Any
from langchain_core.tools import tool
from data.mock_data import ORDERS_DB

@tool
def track_order(order_id: str) -> Dict[str, Any]:
    """Track the status of an order"""
    order_id = order_id.upper()
    if order_id in ORDERS_DB:
        order = ORDERS_DB[order_id]
        
        if order["status"] == "delivered":
            message = f"Order {order_id} was delivered on {order['delivery_date']}."
        elif order["status"] == "shipped":
            message = f"Order {order_id} has been shipped with tracking number {order['tracking']}. Expected delivery: {order['delivery_date']}."
        else:
            message = f"Order {order_id} is being processed. Expected delivery: {order['delivery_date']}."
            
        return {
            "found": True,
            "order_id": order_id,
            "status": order["status"],
            "tracking": order["tracking"],
            "delivery_date": order["delivery_date"],
            "message": message
        }
    
    return {
        "found": False,
        "message": f"I couldn't find order {order_id}. Please check the order number and try again."
    }