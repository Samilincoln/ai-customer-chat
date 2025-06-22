import streamlit as st
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
import config
from utils.helpers import get_response, process_function_call



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

# Sidebar configuration
with st.sidebar:
    st.title("Configuration")
    api_key = st.text_input("Enter Groq API Key", type="password") or config.GROQ_API_KEY
    business_type = st.selectbox(
        "Select Business Type",
        options=config.BUSINESS_TYPES,
        index=config.BUSINESS_TYPES.index(config.DEFAULT_BUSINESS_TYPE)
    )
    
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

# Chat input
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
            else:
                # Process function call if present
                if function_call:
                    st.session_state.function_call_log.append(
                        f"Intent: {function_call['intent']}\nParameters: {function_call['parameters']}"
                    )
                    result = process_function_call(function_call)
                    if result and "Error" not in result:
                        if "message" in result:
                            response_text = result["message"]#.get("response_to_user", " ")
                            # If product not found, try to recommend alternatives
                            if not result.get("found", True) and function_call["intent"] == "check_product_availability":
                                alt_result = process_function_call({
                                    "intent": "recommend_alternatives",
                                    "parameters": {
                                        "product_name": function_call["parameters"]["product_name"]
                                    }
                                })
                                if alt_result and "message" in alt_result:
                                    response_text = f"{response_text}\n\n{alt_result['message']}"
                        else:
                            response_text = "Sorry, I couldn't find that product."
                    else:
                        response_text = result.get("error", "An error occurred while processing your request.")
                
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})