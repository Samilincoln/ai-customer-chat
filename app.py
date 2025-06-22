import streamlit as st
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
import config
from utils.helpers import get_response, process_function_call, generate_business_description



# Page configuration
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.PAGE_LAYOUT
)

st.title("Zita Test")
st.markdown("Chat with our smart customer service agent in English or Pidgin English")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()
if "function_call_log" not in st.session_state:
    st.session_state.function_call_log = []
if "business_description" not in st.session_state:
    st.session_state.business_description = ""
if "show_description" not in st.session_state:
    st.session_state.show_description = False

# Function to generate business description
def update_business_description(business_type, api_key):
    with st.spinner("Generating business description..."):
        description_data = generate_business_description(business_type, api_key)
        if "error" in description_data:
            st.error(description_data["error"])
            return ""
        
        # Format the description as markdown text
        formatted_description = f"## {business_type.title()} Business\n\n"
        formatted_description += f"{description_data.get('description', '')}\n\n"
        
        if "key_operations" in description_data:
            formatted_description += "### Key Operations\n"
            for op in description_data["key_operations"]:
                formatted_description += f"- {op}\n"
            formatted_description += "\n"
        
        if "success_metrics" in description_data:
            formatted_description += "### Success Metrics\n"
            for metric in description_data["success_metrics"]:
                formatted_description += f"- {metric}\n"
            formatted_description += "\n"
            
        if "challenges" in description_data:
            formatted_description += "### Challenges\n"
            for challenge in description_data["challenges"]:
                formatted_description += f"- {challenge}\n"
            formatted_description += "\n"
            
        if "technology_needs" in description_data:
            formatted_description += "### Technology Needs\n"
            for tech in description_data["technology_needs"]:
                formatted_description += f"- {tech}\n"
            formatted_description += "\n"
            
        if "market_trends" in description_data:
            formatted_description += "### Market Trends\n"
            formatted_description += f"{description_data['market_trends']}\n\n"
            
        if "startup_considerations" in description_data:
            formatted_description += "### Startup Considerations\n"
            formatted_description += f"{description_data['startup_considerations']}\n"
            
        return formatted_description

# Sidebar configuration
with st.sidebar:
    st.title("Configuration")
    api_key = st.text_input("Enter Groq API Key", type="password") or config.GROQ_API_KEY
    
    # Business category and type selection with on_change callbacks
    def on_business_category_change():
        # When category changes, reset the business type to the first option in that category
        category = st.session_state.business_category_select
        if category in config.BUSINESS_CATEGORIES:
            # Set the business type to the first option in the selected category
            st.session_state.business_type_select = config.BUSINESS_CATEGORIES[category][0]
            # Update the business description
            st.session_state.show_description = True
            st.session_state.business_description = update_business_description(
                st.session_state.business_type_select,
                api_key
            )
    
    def on_business_type_change():
        st.session_state.show_description = True
        st.session_state.business_description = update_business_description(
            st.session_state.business_type_select, 
            api_key
        )
    
    # First, select the business category
    business_category = st.selectbox(
        "Select Business Category",
        options=list(config.BUSINESS_CATEGORIES.keys()),
        key="business_category_select",
        on_change=on_business_category_change
    )
    
    # Then, select the specific business type from the chosen category
    business_type = st.selectbox(
        "Select Business Type",
        options=config.BUSINESS_CATEGORIES[business_category],
        key="business_type_select",
        on_change=on_business_type_change
    )
    
    # Generate description button
    if st.button("Generate Business Description"):
        st.session_state.show_description = True
        st.session_state.business_description = update_business_description(business_type, api_key)
    
    # Display and make the business description editable
    if st.session_state.show_description:
        st.subheader("Business Description")
        st.session_state.business_description = st.text_area(
            "Edit Description",
            value=st.session_state.business_description,
            height=300
        )
        
        # Option to hide description
        if st.button("Hide Description"):
            st.session_state.show_description = False
    
    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.session_state.memory.clear()
        st.session_state.function_call_log = []
        st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Display function call log in sidebar
with st.sidebar:
    if st.session_state.function_call_log:
        st.subheader("Function Call Log")
        for log in st.session_state.function_call_log:
            st.code(log)

if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text, function_call, error = get_response(
                prompt,
                api_key,
                business_type,
                st.session_state.memory
            )
            
            if error:
                st.error(error)
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {error}"})
            else:
                # Always show the initial LLM response first
                initial_response = response_text
                final_response = response_text
                
                # Display initial response
                if initial_response and initial_response.strip():
                    st.markdown(initial_response)
                    
                # Process function call if present
                if function_call:
                    # Log the function call
                    st.session_state.function_call_log.append(
                        f"Intent: {function_call['intent']}\nParameters: {function_call['parameters']}"
                    )
                    
                    # Show function call indicator
                    with st.spinner(f"Executing: {function_call['intent']}..."):
                        result = process_function_call(function_call)
                        print(f"Function call result: {result}")
                    
                    # Process function call result
                    if result and "Error" not in result:
                        function_response = ""
                        
                        if "message" in result:
                            function_response = result["message"]
                            
                            # Handle specific case for product availability
                            if not result.get("found", True) and function_call["intent"] == "check_product_availability":
                                # Try to get alternatives
                                with st.spinner("Looking for alternatives..."):
                                    alt_result = process_function_call({
                                        "intent": "recommend_alternatives", 
                                        "parameters": {
                                            "product_name": function_call["parameters"]["product_name"]
                                        }
                                    })
                                    
                                    if alt_result and "message" in alt_result:
                                        function_response = f"{function_response}\n\n{alt_result['message']}"
                        else:
                            function_response = "Function executed successfully, but no response message was provided."
                        
                        # Display function result with visual separator
                        if function_response:
                            st.markdown("---")  # Visual separator
                            st.markdown("**Function Result:**")
                            st.markdown(function_response)
                            
                            # Combine responses for chat history
                            if initial_response and initial_response.strip():
                                final_response = f"{initial_response}\n\n---\n\n**Function Result:**\n{function_response}"
                            else:
                                final_response = f"**Function Result:**\n{function_response}"
                    
                    else:
                        # Handle function call error
                        error_message = result.get("error", "An error occurred while processing your request.")
                        st.error(f"Function Error: {error_message}")
                        
                        # Combine with initial response
                        if initial_response and initial_response.strip():
                            final_response = f"{initial_response}\n\n**Note:** There was an issue processing the function call: {error_message}"
                        else:
                            final_response = f"**Error:** {error_message}"
                
                # Add the complete response to chat history
                st.session_state.messages.append({"role": "assistant", "content": final_response})




#=====================version 1=====================
# Chat input
# if prompt := st.chat_input("Type your message here..."):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)
    
#     # Get AI response
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             response_text, function_call, error = get_response(
#                 prompt,
#                 api_key,
#                 business_type,
#                 st.session_state.memory
#             )
            
#             if error:
#                 st.error(error)
#             else:
#                 # Process function call if present
#                 if function_call:
#                     st.session_state.function_call_log.append(
#                         f"Intent: {function_call['intent']}\nParameters: {function_call['parameters']}"
#                     )
#                     result = process_function_call(function_call)
#                     print(result)
#                     if result and "Error" not in result:
#                         if "message" in result:
#                             response_text = result["message"]#.get("response_to_user", " ")
#                             # If product not found, try to recommend alternatives
#                             if not result.get("found", True) and function_call["intent"] == "check_product_availability":
#                                 alt_result = process_function_call({
#                                     "intent": "recommend_alternatives",
#                                     "parameters": {
#                                         "product_name": function_call["parameters"]["product_name"]
#                                     }
#                                 })
#                                 if alt_result and "message" in alt_result:
#                                     response_text = f"{response_text}\n\n{alt_result['message']}"
#                         else:
#                             response_text = "Response Error"
#                     else:
#                         response_text = result.get("error", "An error occurred while processing your request.")
                
#                 st.markdown(response_text)
#                 st.session_state.messages.append({"role": "assistant", "content": response_text})