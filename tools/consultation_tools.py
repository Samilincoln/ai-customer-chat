from typing import Dict, Any, Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from models.schemas import ConsultationParams
from langchain_community.utilities import GoogleSearchAPIWrapper
import os
import json
from datetime import datetime
import config

google_api_key= config.GOOGLE_API_KEY
google_cse_id= config.GOOGLE_CSE_ID


class ConsultationSearchEngine:
    """Handles Google Search operations for consultations"""
    
    def __init__(self, google_api_key: str, google_cse_id: str):
        self.search = GoogleSearchAPIWrapper(
            google_api_key=google_api_key,
            google_cse_id=google_cse_id,
            k=1  # Number of search results
        )
    
    def generate_search_query(self, params: ConsultationParams) -> str:
        """Generate search query based on consultation parameters"""
        query_parts = []
        
        # Add consultation type and subject
        query_parts.append(params.consultation_type)
        query_parts.append(params.subject)
        
        # Add business type if provided
        if params.business_type:
            query_parts.append(params.business_type)
        
        # Add purpose if provided
        if params.purpose:
            query_parts.append(params.purpose)
        
        # Add location if provided
        if params.location:
            query_parts.append(params.location)

        if params.description:
            query_parts.append(params.description)

        if params.budget:
            query_parts.append(params.budget)

        if params.currency:
            query_parts.append(params.currency)
        
        return " ".join(query_parts)
    
    def search_consultation_info(self, query: str) -> Dict[str, Any]:
        """Perform Google search and return structured results"""
        try:
            results = self.search.run(query)
            return {
                "success": True,
                "query": query,
                "results": results,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


def generate_consultation_response(params: ConsultationParams, search_results: Dict[str, Any]) -> str:
    """Generate consultation response based on search results"""
    
    if not search_results["success"]:
        return f"I couldn't find information about {params.subject}. Please try again or contact support."
    
    # Simple response format
    intro = f"Here's what I found about {params.subject}"
    
    if params.location:
        intro += f" in {params.location}"
    
    if params.purpose:
        intro += f" for {params.purpose}"
    
    intro += ":"
    
    return f"{intro}\n\n{search_results['results']}"



@tool
def consultation_service(
    consultation_type: str,
    subject: str, 
    business_type: Optional[str] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
    budget: Optional[float] = None,
    currency: Optional[str] = None,
    purpose: Optional[str] = None
) -> Dict[str, Any]:
    """
    Provide consultation services with Google search integration
    
    Args:
        consultation_type: Type of consultation (property, business, legal, financial, technical, career, health, etc.)
        subject: Main subject or topic of the consultation
        business_type: Type of business or domain (startup, enterprise, healthcare, retail, technology, etc.)
        description: Detailed description of the consultation request and specific requirements
        location: Preferred or relevant location for the consultation
        budget: Budget or financial constraint for the consultation topic
        purpose: Purpose or goal of the consultation (buy, sell, invest, advice, review, planning, etc.)
    
    Returns:
        Dictionary containing consultation response and metadata
    """
    
    # Create consultation parameters
    params = ConsultationParams(
        consultation_type=consultation_type,
        business_type=business_type,
        subject=subject,
        description=description,
        location=location,
        budget=budget,
        currency=float(currency),
        purpose=purpose
    )
    
    # Generate search query
    search_query = search_engine.generate_search_query(params)
    
    # Perform search
    search_results = search_engine.search_consultation_info(search_query)
    
    # Generate consultation response
    consultation_response = generate_consultation_response(params, search_results)
    
    # Prepare response
    response = {
        "success": search_results["success"],
        "consultation_type": params.consultation_type,
        "subject": params.subject,
        "search_query_used": search_query,
        "response": consultation_response,
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "business_type": params.business_type,
            "location": params.location,
            "budget": params.budget,
            "currency": params.currency,
            "purpose": params.purpose,
            "description": params.description
        }
    }
    
    if not search_results["success"]:
        response["error"] = search_results.get("error", "Unknown search error")
    
    return response