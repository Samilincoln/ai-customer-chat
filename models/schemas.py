from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field, field_validator

class FunctionCallParameters(BaseModel):
    """Parameters for a function call"""
    # This is a generic model that will be extended by specific parameter models

class CheckProductAvailabilityParams(FunctionCallParameters):
    """Parameters for check_product_availability function"""
    product_name: str = Field(..., description="Name of the product to check")
    category: Optional[str] = Field(None, description="Category of the product (optional)")

class TrackOrderParams(FunctionCallParameters):
    """Parameters for track_order function"""
    order_id: str = Field(..., description="Order ID to track")

class ApplyDiscountParams(FunctionCallParameters):
    """Parameters for apply_discount function"""
    product_name: str = Field(..., description="Name of the product to apply discount to")
    discount_code: str = Field(..., description="Discount code to apply")

class RecommendAlternativesParams(FunctionCallParameters):
    """Parameters for recommend_alternatives function"""
    product_name: str = Field(..., description="Name of the product to find alternatives for")

class HandleNegotiationParams(FunctionCallParameters):
    """Parameters for handle_negotiation function"""
    product_name: str = Field(..., description="Name of the product being negotiated")
    business_type: str = Field(..., description="Type of business")
    offered_price: float = Field(..., description="Price offered by the customer")
    max_price: Optional[float] = Field(None, description="Maximum acceptable price (first offer)")
    min_price: Optional[float] = Field(None, description="Minimum acceptable price")

class ConsultationParams(FunctionCallParameters):
    """Parameters for property_consultation function"""
    consultation_type: Optional[str] = Field(...,description="Type of consultation (property, business, legal, financial, technical, career, health, etc.)")
    business_type: Optional[str] = Field(None, description="Type of business or domain (startup, enterprise, healthcare, retail, technology, etc.)")
    subject: Optional[str] = Field(..., description="Main subject or topic of the consultation")
    description: Optional[str] = Field(None, description="Detailed description of the consultation request and specific requirements")
    location: Optional[str] = Field(None, description="Preferred or relevant location for the consultation")
    budget: Optional[float] = Field(None, description="Budget or financial constraint for the consultation topic")
    currency: Optional[str] = Field(None, description="Currency for the budget (e.g., USD, EUR, GBP)")
    purpose: Optional[str] = Field(None, description="Purpose or goal of the consultation (buy, sell, invest, advice, review, planning, etc.)")

class FunctionCall(BaseModel):
    """Function call with intent and parameters"""
    intent: str = Field(..., description="Intent of the function call")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parameters for the function call")
    
    @field_validator('intent')
    @classmethod
    def validate_intent(cls, v):
        if v is None:
            raise ValueError("Intent cannot be None")
        return v

class LLMResponse(BaseModel):
    """Response from the LLM"""
    response_to_user: str = Field(..., description="Response to show to the user")
    function_call: Optional[FunctionCall] = Field(None, description="Function call to execute")