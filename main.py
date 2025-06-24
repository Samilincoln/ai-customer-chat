from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import os
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from config import BUSINESS_CATEGORIES
from decouple import config
from utils import get_response, process_function_call, generate_business_description
import uuid

# Initialize FastAPI app
app = FastAPI(
    title="Zita API",
    description="API for Zita customer service agent",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    business_type: str
    #api_key: Optional[str] = None

class BusinessDescriptionRequest(BaseModel):
    business_type: str
    #api_key: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    function_call: Optional[Dict] = None
    function_result: Optional[Dict] = None
    detected_intent: Optional[str] = None

class BusinessDescriptionResponse(BaseModel):
    description: str

# In-memory storage for chat sessions
chat_sessions = {}

# Helper function to get or create a chat session
def get_chat_session(session_id: str):
    if session_id not in chat_sessions:
        chat_sessions[session_id] = {
            "messages": [],
            "memory": ConversationBufferMemory(),
            "function_call_log": []
        }
    return chat_sessions[session_id]

# Format business description (similar to the Streamlit app)
def format_business_description(description_data):
    if "error" in description_data:
        raise HTTPException(status_code=400, detail=description_data["error"])
        
    business_type = description_data.get("business_type", "Business")
    formatted_description = f"## {business_type.title()} Business\n\n"
    formatted_description += f"{description_data.get('description', '')}\n\n"
    
    if "key_operations" in description_data:
        formatted_description += "### Key Operations\n"
        for op in description_data["key_operations"]:
            formatted_description += f"- {op}\n"
        formatted_description += "\n"
        
    return formatted_description

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to Zita API. Use /docs to see available endpoints."}

@app.post("/chat/{session_id}", response_model=ChatResponse)
async def chat(
    session_id: str,
    request: ChatRequest
):
    # Get or create chat session
    session = get_chat_session(session_id)
    
    # Use provided API key or fallback to config
    api_key = config("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=400, detail="API key is required")
    
    # Get response from AI
    response_text, function_call, detected_intent, error = get_response(
        request.message,
        api_key,
        request.business_type,
        session["memory"]
    )
    
    # Handle error
    if error:
        raise HTTPException(status_code=500, detail=str(error))
    
    # Initialize response
    result = {
        "response": response_text,
        "function_call": function_call,
        "function_result": None,
        "detected_intent": detected_intent,
    }
    
    # Process function call if present
    if function_call:
        # Log the function call
        session["function_call_log"].append(
            f"Intent: {function_call['intent']}\nParameters: {function_call['parameters']}"
        )
        
        # Execute function call
        function_result = process_function_call(function_call)
        
        # Process function call result
        if function_result and "Error" not in function_result:
            function_response = ""
            
            if "message" in function_result:
                function_response = function_result["message"]
                
                # Handle specific case for product availability
                if not function_result.get("found", True) and function_call["intent"] == "check_product_availability":
                    # Try to get alternatives
                    alt_result = process_function_call({
                        "intent": "recommend_alternatives", 
                        "parameters": {
                            "product_name": function_call["parameters"]["product_name"]
                        }
                    })
                    
                    if alt_result and "message" in alt_result:
                        function_response = f"{function_response}\n\n{alt_result['message']}"
                        function_result["alternatives"] = alt_result
            
            # Update response with function result
            if response_text and response_text.strip():
                final_response = f"{response_text}\n\n---\n\n**Function Result:**\n{function_response}"
            else:
                final_response = f"**Function Result:**\n{function_response}"
            
            result["response"] = final_response
            result["function_result"] = function_result
        else:
            # Handle function call error
            error_message = function_result.get("error", "An error occurred while processing your request.")
            
            # Combine with initial response
            if response_text and response_text.strip():
                final_response = f"{response_text}\n\n**Note:** There was an issue processing the function call: {error_message}"
            else:
                final_response = f"**Error:** {error_message}"
            
            result["response"] = final_response
            result["function_result"] = {"error": error_message}
    
    # Add to chat history
    session["messages"].append({"role": "user", "content": request.message})
    session["messages"].append({"role": "assistant", "content": result["response"]})
    
    return result

@app.post("/business-description", response_model=BusinessDescriptionResponse)
async def get_business_description(request: BusinessDescriptionRequest):
    # Use provided API key or fallback to config
    api_key = config("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=400, detail="API key is required")
    
    # Generate business description
    description_data = generate_business_description(request.business_type, api_key)
    
    # Format the description
    formatted_description = format_business_description(description_data)
    
    return {"description": formatted_description}

@app.get("/chat-history/{session_id}")
async def get_chat_history(session_id: str):
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"messages": chat_sessions[session_id]["messages"]}

@app.delete("/chat-history/{session_id}")
async def clear_chat_history(session_id: str):
    if session_id in chat_sessions:
        chat_sessions[session_id] = {
            "messages": [],
            "memory": ConversationBufferMemory(),
            "function_call_log": []
        }
    
    return {"message": "Chat history cleared"}

@app.get("/business-categories")
async def get_business_categories():
    return {"categories": BUSINESS_CATEGORIES}

@app.get("/function-call-log/{session_id}")
async def get_function_call_log(session_id: str):
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"function_call_log": chat_sessions[session_id]["function_call_log"]}

@app.post("/create-session")
async def create_session():
    # Generate a unique session ID
    session_id = str(uuid.uuid4())
    
    # Initialize the session
    get_chat_session(session_id)
    
    return {"session_id": session_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)