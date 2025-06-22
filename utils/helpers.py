import json
import re
from typing import Dict, Any, Optional, Tuple
from Zita.models.schemas import LLMResponse, FunctionCallParameters
#from .models import LLMResponse, FunctionCallParameters





def generate_zita_prompt(business_type: str) -> str:
    """Generate Zita's prompt for different business types"""
    from Zita.data.mock_data import PRODUCT_DB
    
    sector_prompts = {
    # PRODUCTS - Physical Goods
    "online_clothing_store": "helping customers find clothing items, providing size guides, checking inventory, handling orders and returns, offering styling advice, processing payments, managing delivery tracking",    
    "gadget_shop": "advising on gadget features and specifications, checking product availability, providing pricing information, handling warranty inquiries, assisting with order tracking, offering technical support guidance",    
    "general_ecommerce_store": "answering product questions, checking availability, processing orders, handling returns and exchanges, providing shipping information, managing customer complaints, offering product recommendations",    
    "niche_product_seller": "providing specialized product knowledge, explaining unique features, checking inventory, handling custom orders, managing deliveries, offering expert advice, processing payments",    
    "packaged_snacks_brand": "providing product information, checking availability, handling bulk orders, explaining nutritional content, managing distribution inquiries, processing orders, handling complaints",    
    "food_beverage_production": "providing product specifications, handling wholesale inquiries, managing distribution partnerships, explaining ingredients and nutritional information, processing large orders, handling quality concerns",    
    "wig_hair_vendor": "helping customers choose hair types and textures, providing styling advice, checking availability, handling orders and returns, offering care instructions, managing custom orders",
    "skincare_brand": "advising on skincare routines, explaining product ingredients, providing usage instructions, handling orders and returns, answering skin concern questions, managing subscription services",    
    "pharmacy": "providing medication information, checking prescription status, explaining drug interactions, handling insurance inquiries, managing refill requests, offering health consultations",
    "nutrition_brand": "explaining supplement benefits, providing dosage information, checking product availability, handling orders, answering health-related questions, managing subscription services",    
    "hardware_sales_repairs": "providing technical specifications, checking parts availability, offering repair services, handling warranty claims, providing installation guidance, managing service appointments",    
    "software_sales_licensing": "explaining software features, providing licensing information, handling installation support, managing subscription renewals, offering technical assistance, processing enterprise orders",    
    "furniture_manufacturer": "showcasing furniture options, providing dimensions and specifications, handling custom orders, managing delivery schedules, offering assembly services, handling warranty claims",    
    "textile_producer": "providing fabric specifications, handling bulk orders, offering samples, managing production timelines, explaining care instructions, processing wholesale inquiries",    
    "soap_detergent_maker": "explaining product ingredients, providing usage instructions, handling bulk orders, managing distribution inquiries, offering custom formulations, processing orders",    
    "agro_processor": "providing product specifications, handling bulk orders, managing supply chain inquiries, explaining processing methods, offering quality certifications, coordinating deliveries",    
    "poultry_farm": "providing product availability, handling wholesale orders, explaining farming practices, managing delivery schedules, offering quality certifications, processing payments",    
    "crop_farm": "checking produce availability, handling wholesale orders, providing harvest schedules, managing delivery logistics, offering quality certifications, coordinating bulk purchases",    
    "agricultural_tools_reseller": "explaining tool specifications, checking availability, providing usage guidance, handling orders and returns, offering maintenance services, managing warranties",    
    "fish_farming": "providing product availability, handling wholesale orders, explaining farming methods, managing delivery schedules, offering quality certifications, processing bulk orders",    
    "jewelry_maker": "showcasing jewelry designs, handling custom orders, providing material specifications, managing repair services, offering sizing services, processing payments",    
    "craft_supplies_seller": "providing product information, checking inventory, handling orders, offering project guidance, managing bulk purchases, processing educational institution orders",
    # SERVICES - Food & Hospitality
    "restaurant": "taking food orders, providing menu information, handling reservations, managing delivery requests, answering dietary questions, processing payments, handling complaints",    
    "food_vendor": "providing menu details, taking orders, giving delivery information, handling special dietary requests, managing event catering, processing payments, tracking orders",
    # SERVICES - Real Estate
    "real_estate_agent": "showing available properties, providing property details, scheduling viewings, explaining purchase processes, handling negotiations, offering market insights, managing documentation",    
    "property_manager": "handling tenant inquiries, managing maintenance requests, processing rent payments, scheduling inspections, handling lease renewals, managing property viewings",    
    "shortlet_apartment_service": "checking availability, providing booking information, handling reservations, explaining amenities, managing check-in processes, processing payments, handling guest requests",    
    "land_seller": "providing land details, explaining zoning information, handling purchase inquiries, scheduling site visits, managing documentation, offering financing options, processing transactions",
    # SERVICES - Fashion & Beauty
    "tailor_fashion_designer": "discussing design options, taking measurements, providing fabric choices, handling custom orders, scheduling fittings, managing alterations, processing payments",    
    "makeup_artist": "explaining makeup services, providing portfolio examples, handling booking appointments, discussing event requirements, offering makeup consultations, managing scheduling",
    # SERVICES - Health & Wellness
    "private_clinic": "scheduling appointments, providing medical information, handling insurance inquiries, managing patient records, explaining procedures, processing payments, handling referrals",    
    "fitness_coach": "explaining training programs, scheduling sessions, providing nutrition advice, handling membership inquiries, managing progress tracking, offering consultation services",    
    "mental_health_coach": "explaining therapy approaches, scheduling sessions, handling confidentiality concerns, providing crisis support resources, managing appointment bookings, offering consultation services",
    # SERVICES - Education
    "private_tutor": "explaining subject expertise, scheduling lessons, providing learning materials, handling payment arrangements, tracking student progress, offering assessment services",    
    "online_course_creator": "explaining course content, handling enrollment, providing access instructions, managing technical support, offering certification information, processing payments",    
    "study_abroad_coach": "providing application guidance, explaining program options, handling document preparation, offering visa assistance, managing consultation bookings, providing country information",    
    "edtech_platform": "explaining platform features, handling user registration, providing technical support, managing subscription services, offering training resources, processing educational institution orders",
    # SERVICES - Events & Entertainment
    "event_planner": "discussing event requirements, providing venue options, handling vendor coordination, managing timelines, offering package deals, processing bookings and payments",    
    "mc_host": "explaining services offered, checking availability, providing portfolio examples, handling event bookings, discussing requirements, managing performance schedules",    
    "dj_band": "showcasing music repertoire, checking availability, discussing event requirements, handling bookings, providing equipment information, managing performance schedules",    
    "wedding_vendor": "explaining wedding packages, checking availability, providing portfolio examples, handling bookings, coordinating with other vendors, managing payment schedules",
    # SERVICES - Business & Finance
    "tax_consultant": "explaining tax services, scheduling consultations, providing compliance guidance, handling document preparation, offering advisory services, managing filing deadlines",    
    "grant_writer": "explaining grant writing services, discussing eligibility requirements, handling proposal development, managing application timelines, providing success metrics, offering consultation services",    
    "bookkeeper": "explaining accounting services, handling financial record management, providing reporting services, managing payroll processing, offering tax preparation, scheduling consultations",    
    "legal_regulatory_consultant": "explaining legal services, providing compliance guidance, handling document preparation, offering advisory consultations, managing case requirements, scheduling appointments",
    # SERVICES - Technology
    "web_development_agency": "explaining development services, providing portfolio examples, handling project requirements, managing timelines, offering maintenance services, processing project payments",    
    "saas_startup": "explaining software features, handling subscription management, providing technical support, managing user onboarding, offering integration services, processing enterprise inquiries",    
    "app_developer": "explaining development services, providing portfolio examples, handling project requirements, managing development timelines, offering maintenance services, processing payments",    
    "cybersecurity_consultant": "explaining security services, providing risk assessments, handling compliance requirements, offering training services, managing security audits, scheduling consultations",    
    "cloud_networking_provider": "explaining service offerings, providing technical specifications, handling infrastructure requirements, managing service provisioning, offering support services, processing enterprise orders",
    # SERVICES - Business Consulting
    "business_strategy_consultant": "explaining consulting services, providing case studies, handling project requirements, managing consultation schedules, offering strategic guidance, processing service agreements",    
    "hr_recruitment_consultant": "explaining recruitment services, handling job postings, managing candidate screening, providing HR advisory services, offering training programs, processing service agreements",    
    "legal_advisory": "explaining legal services, providing case consultation, handling document review, offering compliance guidance, managing legal processes, scheduling appointments",    
    "compliance_specialist": "explaining compliance requirements, providing regulatory guidance, handling audit preparation, offering training services, managing compliance processes, scheduling consultations",
    # SERVICES - Logistics & Transport
    "courier_dispatch_service": "handling pickup and delivery requests, providing tracking information, managing scheduling, offering pricing quotes, handling special delivery requirements, processing payments",    
    "trucking_company": "handling freight inquiries, providing shipping quotes, managing delivery schedules, offering tracking services, handling special cargo requirements, processing logistics payments",    
    "freight_forwarding": "managing international shipping, providing customs documentation, handling cargo tracking, offering logistics solutions, managing delivery coordination, processing shipping payments",    
    "delivery_bike_operator": "handling local delivery requests, providing time estimates, managing pickup schedules, offering rush delivery services, tracking delivery status, processing payment",
    # SERVICES - Marketing & Media
    "pr_agency": "explaining PR services, providing campaign examples, handling media relations, managing crisis communication, offering brand strategy, processing service agreements",    
    "influencer_manager": "explaining talent management services, providing influencer portfolios, handling brand partnerships, managing campaign coordination, offering strategy services, processing agreements",    
    "content_creation_studio": "explaining content services, providing portfolio examples, handling project requirements, managing production timelines, offering strategy consultation, processing creative payments",    
    "podcast_producer": "explaining production services, providing equipment specifications, handling recording schedules, managing editing services, offering distribution guidance, processing production payments",
    # SERVICES - Travel & Hospitality
    "hotel": "handling room reservations, providing amenity information, managing check-in processes, offering concierge services, handling special requests, processing booking payments",    
    "shortlet_manager": "checking property availability, handling booking inquiries, managing guest communications, providing property information, coordinating check-in processes, processing rental payments",    
    "travel_agency": "providing travel packages, handling flight and accommodation bookings, offering travel insurance, managing itinerary planning, providing destination information, processing travel payments",    
    "travel_abroad_consultant_visa_agent": "explaining visa requirements, handling application processes, providing document guidance, offering travel consultation, managing appointment scheduling, processing service fees",
    # SERVICES - Creative & Construction
    "portrait_artist": "explaining artistic services, providing portfolio examples, handling commission requests, managing sitting schedules, offering framing services, processing artistic payments",    
    "interior_decor_artist": "explaining design services, providing portfolio examples, handling consultation requests, managing project timelines, offering procurement services, processing design payments",    
    "civil_engineer": "explaining engineering services, providing project consultation, handling technical requirements, managing project timelines, offering inspection services, processing professional fees",    
    "building_contractor": "providing construction services, handling project estimates, managing construction timelines, offering material procurement, coordinating subcontractors, processing construction payments",    
    "electrician": "explaining electrical services, handling service requests, providing safety inspections, managing appointment scheduling, offering emergency services, processing service payments",    
    "plumber": "explaining plumbing services, handling service requests, providing maintenance services, managing emergency calls, offering installation services, processing service payments",
    "surveyor": "explaining surveying services, handling property assessments, providing technical reports, managing site visits, offering consultation services, processing professional fees",   
    "other_unique_niche_services": "explaining specialized services, providing service details, handling custom requirements, managing consultation schedules, offering expert guidance, processing service payments"
}
    
    tasks = sector_prompts.get(business_type.lower(), "assisting customers with general inquiries, sales, and complaints")

    # Define the available tools
    available_tools = [
        {
            "intent": "check_product_availability",
            "description": "Check if a product is available and get price information",
            "parameters": ["product_name", "category (optional)"]
        },
        {
            "intent": "track_order",
            "description": "Track an order status and delivery information",
            "parameters": ["order_id"]
        },
        {
            "intent": "apply_discount",
            "description": "Apply a discount code to a product",
            "parameters": ["product_name", "discount_code"]
        },
        {
            "intent": "recommend_alternatives",
            "description": "Recommend alternative products when a requested item is out of stock",
            "parameters": ["product_name"]
        },
        {
            "intent": "handle_negotiation",
            "description": "Handle price negotiations for products",
            "parameters": ["product_name", "offered_price", "max_price (optional)", "min_price (optional)"]
        },
        {
            "intent": "consultation_service",
            "description": "Handle consultaion with external information from the web",
            "parameters": ["consultation_type", "subject", "business_type (optional)", "description (optional)","location (optional)","budget (optional)","purpose (optional)"]
        }
    ]
    
    tools_description = "\n".join([
        f"- {tool['intent']}: {tool['description']} (Parameters: {', '.join(tool['parameters'])})"
        for tool in available_tools
    ])

    # Add available product categories to the prompt
    available_categories = ", ".join(PRODUCT_DB.keys())
    
    prompt_text = f"""
    You are Zita, a conversational customer care and sales assistant for a business in the {business_type} sector.
    You're trained to handle chats in either Nigerian Pidgin English or English.
    Default to English unless the customer writes in real Nigerian Pidgin (not just typos or grammar mistakes).
    When in Pidgin, reply in a warm, street-wise but respectful tone. When in English, use friendly and professional language.

    Your job is to help customers with tasks such as: {tasks}.

    You have the following functions available that you can use:
    {tools_description}

    For each customer message, determine if you need to call a function from the customer's intent. If yes, respond in the following JSON format:
    {{
        "response_to_user": "your friendly response to the user",
        "function_call": {{
            "intent": "one of the available intents listed above",
            "parameters": {{
                "parameter1": "value1",
                "parameter2": "value2"
            }}
        }}
    }}

    If no function call is needed, respond in this format:
    {{
        "response_to_user": "your friendly response to the user",
        "function_call": null
    }}

    IMPORTANT: 
    -   Your response MUST be a valid JSON object that can be parsed by Python's json.loads() function.
        Keep your "response_to_user" natural, conversational and helpful. Never mention JSON or that you're calling functions.
        All responses must be in the described JSON format.
    -   You MUST ALWAYS check the product database before responding about product availability or details.
        The store only sells products in these categories: {available_categories}.
    -   If product is out of stock in {available_categories}, recommend alternatives in {available_categories}.
    -   NEVER make up information about products that aren't in the database.
    """

    return prompt_text.strip()

#===============version 3====================
def parse_llm_response(response_text: str) -> Dict[str, Any]:
    """Parse the LLM response to extract function call and user response"""
    try:
        # Try to parse the entire response as JSON
        response_data = json.loads(response_text)
        print(response_data)
        # Validate with Pydantic model
        return LLMResponse(**response_data).model_dump()
    except json.JSONDecodeError:
        # If that fails, try to extract JSON from the text
        try:
            # Look for JSON-like structure between braces
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                response_data = json.loads(json_match.group(0))
                
                # Ensure response_to_user is always present
                if 'response_to_user' not in response_data:
                    response_data['response_to_user'] = response_text
                
                # Validate function_call if present
                if 'function_call' in response_data:
                    func_call = response_data['function_call']
                    if isinstance(func_call, dict):
                        # Ensure function_call has required fields
                        if 'intent' not in func_call:
                            # Remove invalid function_call
                            response_data.pop('function_call')
                        else:
                            # Ensure parameters is a dictionary
                            if 'parameters' not in func_call or not isinstance(func_call['parameters'], dict):
                                func_call['parameters'] = {}
                
                # Validate with Pydantic model
                return LLMResponse(**response_data).model_dump()
            
        except (json.JSONDecodeError, AttributeError):
            pass
    
    # If all parsing attempts fail, return as direct response
    return LLMResponse(
        response_to_user=response_text,
        function_call=None
    ).model_dump()


#===========version 2=============
# def parse_llm_response(response_text: str) -> Dict[str, Any]:
#     """Parse the LLM response to extract function call and user response"""
#     try:
#         # Try to parse the entire response as JSON
#         response_data = json.loads(response_text)
#         # Validate with Pydantic model
#         return LLMResponse(**response_data).model_dump()
#     except json.JSONDecodeError:
#         # If that fails, try to extract JSON from the text
#         try:
#             # Look for JSON-like structure between braces
#             json_match = re.search(r'\{[\s\S]*\}', response_text)
#             if json_match:
#                 response_data = json.loads(json_match.group(0))
                
#                 # Additional validation for function_call parameters
#                 if 'function_call' in response_data:
#                     func_call = response_data['function_call']
#                     if isinstance(func_call, dict):
#                         # Ensure parameters is a dictionary
#                         if 'parameters' in func_call and not isinstance(func_call['parameters'], dict):
#                             # Convert malformed parameters to proper format
#                             params = func_call['parameters']
#                             if isinstance(params, str):
#                                 # If it's a string, assume it's the category
#                                 func_call['parameters'] = {"category": params}
#                             else:
#                                 # Remove invalid parameters
#                                 func_call['parameters'] = {}
#                 elif 'response_to_user' in response_data:
#                     # If only response_to_user is present, return it as a direct response
#                     return LLMResponse(
#                         response_to_user=response_data['response_to_user'],
#                         function_call=None
#                     ).model_dump()
                
#                 # Validate with Pydantic model
#                 return LLMResponse(**response_data).model_dump()
#         except (json.JSONDecodeError, AttributeError):
#             pass
    
#     # If all parsing attempts fail or if the response doesn't look like a function call,
#     # return it as a direct response to the user
#     return LLMResponse(
#         response_to_user=response_text,
#         function_call=None
#     ).model_dump()


#===========version 1=============
# def parse_llm_response(response_text: str) -> Dict[str, Any]:
#     """Parse the LLM response to extract function call and user response"""
#     try:
#         # Try to parse the entire response as JSON
#         response_data = json.loads(response_text)
#         # Validate with Pydantic model
#         return LLMResponse(**response_data).model_dump()
#     except json.JSONDecodeError:
#         # If that fails, try to extract JSON from the text
#         try:
#             # Look for JSON-like structure between braces
#             json_match = re.search(r'\{[\s\S]*\}', response_text)
#             if json_match:
#                 response_data = json.loads(json_match.group(0))
#                 # Validate with Pydantic model
#                 return LLMResponse(**response_data).model_dump()
#         except (json.JSONDecodeError, AttributeError):
#             pass
    
#     # If all parsing attempts fail, return a default structure
#     return LLMResponse(
#         response_to_user=response_text,
#         function_call=None
#     ).model_dump()


def process_function_call(function_call: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Process a function call based on intent and parameters"""
    if not function_call:
        return None
    
    from Zita.tools.product_tools import check_product_availability, recommend_alternatives, apply_discount
    from Zita.tools.order_tools import track_order
    from Zita.tools.negotiation_tools import handle_negotiation
    from Zita.tools.consultation_tools import consultation_service
    from Zita.models.schemas import (
        CheckProductAvailabilityParams, TrackOrderParams, 
        ApplyDiscountParams, RecommendAlternativesParams,
        HandleNegotiationParams,ConsultationParams,
    )
    
    intent = function_call.get("intent")
    parameters = function_call.get("parameters", {})
    
    # Map of available tools and their parameter models
    available_tools = {
        "check_product_availability": (check_product_availability, CheckProductAvailabilityParams),
        "track_order": (track_order, TrackOrderParams),
        "apply_discount": (apply_discount, ApplyDiscountParams),
        "recommend_alternatives": (recommend_alternatives, RecommendAlternativesParams),
        "handle_negotiation": (handle_negotiation, HandleNegotiationParams),
        "consultation_service": (consultation_service, ConsultationParams)
    }
    
    if intent not in available_tools:
        return {"error": f"Unknown intent: {intent}"}
    
    tool_func, param_model = available_tools[intent]
    
    try:
        # Validate parameters with the appropriate Pydantic model
        validated_params = param_model(**parameters).model_dump()
        # Remove None values
        validated_params = {k: v for k, v in validated_params.items() if v is not None}
        
        # Execute the tool function with validated parameters
        try:
            if hasattr(tool_func, 'run'):
                param_str = " ".join([f"{k}={repr(v)}" for k, v in validated_params.items()])
                result = tool_func.run(param_str)
            else:
                result = tool_func(**validated_params)
            return result
        except Exception as e:
            return {"error": f"Error executing {intent}: {str(e)}"}
            
    except Exception as e:
        return {"error": f"Error validating parameters for {intent}: {str(e)}"}


def get_response(user_input: str, api_key: str, business_type: str, memory=None) -> Tuple[str, Optional[Dict[str, Any]], Optional[str]]:
    """Generate LLM response and process any function calls"""
    if not api_key:
        return "⚠️ Please enter a valid API key.", None, None
    
    try:
        # Generate the prompt based on business type
        zita_prompt = generate_zita_prompt(business_type)
        
        # Initialize LLM client
        from langchain_groq import ChatGroq
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name="llama3-70b-8192"
        )
        
        # Build conversation history if memory is provided
        conversation_history = ""
        if memory and hasattr(memory, "buffer") and memory.buffer:
            conversation_history = memory.buffer
        
        # Create prompt with conversation history and user input
        if conversation_history:
            prompt_text = f"{zita_prompt}\n\n{conversation_history}\nCustomer: {user_input}\nZita:"
        else:
            prompt_text = f"{zita_prompt}\n\nCustomer: {user_input}\nZita:"
        
        # Get LLM response
        raw_response = llm.invoke(prompt_text)
        
        # Parse the response
        parsed_response = parse_llm_response(raw_response.content)
        
        # Get the response to show to the user
        response_to_user = parsed_response.get("response_to_user")
        
        # Update memory if provided
        if memory:
            memory.save_context({"input": f"Customer: {user_input}"}, {"output": f"Zita: {response_to_user}"})
        
        # Process function call if present
        function_call = parsed_response.get("function_call")
        detected_intent = None
        function_result = None
        
        if function_call:
            detected_intent = function_call.get("intent")
            function_result = process_function_call(function_call)
            
            # If we have a function result with a message, append it to the response
            if function_result and "message" in function_result:
                response_to_user += f"\n\n{function_result['message']}"
                # Update memory with function result if provided
                if memory:
                    memory.save_context({"input": ""}, {"output": f"Zita: {function_result['message']}"})
        
        return response_to_user, function_call, detected_intent, None
    
    except Exception as e:
        return f"⚠️ Error: {str(e)}", None,None, str(e)



# import config

# google_api_key= config.GOOGLE_API_KEY
# google_cse_id= config.GOOGLE_CSE_ID


# class ConsultationSearchEngine:
#     """Handles Google Search operations for consultations"""
    
#     def __init__(self, google_api_key: str, google_cse_id: str):
#         self.search = GoogleSearchAPIWrapper(
#             google_api_key=google_api_key,
#             google_cse_id=google_cse_id,
#             k=5  # Number of search results
#         )
    
#     def generate_search_query(self, params: ConsultationParams) -> str:
#         """Generate search query based on consultation parameters"""
#         query_parts = []
        
#         # Add consultation type and subject
#         query_parts.append(params.consultation_type)
#         query_parts.append(params.subject)
        
#         # Add business type if provided
#         if params.business_type:
#             query_parts.append(params.business_type)
        
#         # Add purpose if provided
#         if params.purpose:
#             query_parts.append(params.purpose)
        
#         # Add location if provided
#         if params.location:
#             query_parts.append(params.location)
        
#         return " ".join(query_parts)
    
#     def search_consultation_info(self, query: str) -> Dict[str, Any]:
#         """Perform Google search and return structured results"""
#         try:
#             results = self.search.run(query)
#             return {
#                 "success": True,
#                 "query": query,
#                 "results": results,
#                 "timestamp": datetime.now().isoformat()
#             }
#         except Exception as e:
#             return {
#                 "success": False,
#                 "query": query,
#                 "error": str(e),
#                 "timestamp": datetime.now().isoformat()
#             }


# def generate_consultation_response(params: ConsultationParams, search_results: Dict[str, Any]) -> str:
#     """Generate consultation response based on search results"""
    
#     if not search_results["success"]:
#         return f"I couldn't find information about {params.subject}. Please try again or contact support."
    
#     # Simple response format
#     intro = f"Here's what I found about {params.subject}"
    
#     if params.location:
#         intro += f" in {params.location}"
    
#     if params.purpose:
#         intro += f" for {params.purpose}"
    
#     intro += ":"
    
#     return f"{intro}\n\n{search_results['results']}"


# def get_response(user_input: str, api_key: str, business_type: str) -> Tuple[str, Optional[Dict[str, Any]], Optional[str]]:
#     """Generate LLM response and process any function calls"""
#     if not api_key:
#         return "⚠️ Please enter a valid API key.", None, None
    
#     try:
#         # Generate the prompt based on business type
#         zita_prompt = generate_zita_prompt(business_type)
        
#         # Initialize LLM client
#         from langchain_groq import ChatGroq
#         llm = ChatGroq(
#             groq_api_key=api_key,
#             model_name="llama3-70b-8192"
#         )
        
#         # Create prompt with user input
#         prompt_text = f"{zita_prompt}\n\nCustomer: {user_input}\nZita:"
        
#         # Get LLM response
#         raw_response = llm.invoke(prompt_text)
        
#         # Parse the response
#         parsed_response = parse_llm_response(raw_response.content)
        
#         # Get the response to show to the user
#         response_to_user = parsed_response.get("response_to_user")#, raw_response.content)
        
#         # Process function call if present
#         function_call = parsed_response.get("function_call")
#         detected_intent = None
#         function_result = None
        
#         if function_call:
#             detected_intent = function_call.get("intent")
#             function_result = process_function_call(function_call)
            
#             # If we have a function result with a message, append it to the response
#             if function_result and "message" in function_result:
#                 response_to_user += f"\n\n{function_result['message']}"
        
#         return response_to_user, function_result, detected_intent
    
#     except Exception as e:
#         return f"⚠️ Error: {str(e)}", None, None


def generate_business_description(business_type: str, api_key: str) -> Dict[str, Any]:
    """
    Generate a comprehensive business description using LLM based on the business sector
    
    Args:
        business_type: The type of business sector (e.g., "e-commerce", "banking")
        api_key: The Groq API key for LLM access
        
    Returns:
        A dictionary containing the business description and related information
    """
    if not api_key:
        return {"error": "⚠️ Please enter a valid API key."}
    
    try:
        # Initialize LLM client
        from langchain_groq import ChatGroq
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name="llama3-70b-8192"
        )
        
        # Create a detailed prompt for business description generation
        prompt_text = f"""
        Generate a comprehensive business description for a business in the {business_type} sector.
        
        Please structure your response as a JSON object with the following fields:
        1. "description": A detailed paragraph describing the business type, its main activities, and value proposition
        2. "key_operations": An array of strings listing the main operational activities of this business type
        
        Ensure your response is factual, comprehensive, and directly relevant to the {business_type} sector.
        Ensure your response is as you are part of the organization.
        The response must be a valid JSON object that can be parsed by Python's json.loads() function.
        """
        
        # Get LLM response
        raw_response = llm.invoke(prompt_text)
        
        # Parse the JSON response
        try:
            # Try to parse the entire response as JSON
            response_data = json.loads(raw_response.content)
            return response_data
        except json.JSONDecodeError:
            # If that fails, try to extract JSON from the text
            try:
                # Look for JSON-like structure between braces
                json_match = re.search(r'\{[\s\S]*\}', raw_response.content)
                if json_match:
                    response_data = json.loads(json_match.group(0))
                    return response_data
            except (json.JSONDecodeError, AttributeError):
                pass
        
        # If JSON parsing fails, return a structured error response
        return {
            "error": "Failed to parse LLM response as JSON",
            "raw_response": raw_response.content
        }
    
    except Exception as e:
        return {"error": f"⚠️ Error: {str(e)}"}
