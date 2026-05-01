import streamlit as st
import requests
import json

st.set_page_config(page_title="BareBones RAG", layout="centered")
st.title("BareBonesRAG")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask anything from uploaded docs..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call your API
    with st.spinner("Thinking..."):
        try:
            # 1. Prepare the JSON payload that matches the backend's QueryRequest model
            payload = {
                "query": prompt,
                "history": st.session_state.messages  # This sends the full conversation
            }
            
            # 2. Use requests.post instead of requests.get
            response = requests.post(
                "http://127.0.0.1:8000/answer", 
                json=payload  # 'json=' automatically sets headers to application/json
            )
            
            # 3. Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "Error: No answer received")
                sources = data.get("sources", [])
                
                # Display assistant response
                with st.chat_message("assistant"):
                    st.markdown(answer)
                    
                    if sources:
                        with st.expander("🔍 View Sources"):
                            for i, source in enumerate(sources):
                                st.caption(f"**Source {i+1}:** {source[:200]}...")

                # Add assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"Backend Error: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Could not connect to backend. Error: {e}")