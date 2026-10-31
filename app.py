import streamlit as st
from google import genai

client=genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
# for model in client.models.list():
#     print(f"Model ID: {model.name} -> Display: {model.display_name}")

# Inject CSS to flip user message alignment
st.markdown("""
<style>
/* Target the user message container and reverse row layout */
div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {
    flex-direction: row-reverse;
    text-align: right;
    margin-left: auto;
    width: fit-content;
    max-width: 80%;
    border: 2px solid #e0e0e0;       /* Adds a slight, clean light-gray border */
    border-radius: 10px;              /* Rounds the sharp corners of the border */
    padding: 8px 10px;              /* Gives breathing room between the text and the border */
    background-color: #D3D3D3;
    white-space: pre-wrap;
}
/* Only show the note when the placeholder is actively visible */
div[data-testid="stChatInput"]:has(textarea[placeholder]:placeholder-shown)::after {
    content: "Shift + Enter for new line";
    font-size: 0.75rem;
    color: #a0a0a0;
    position: absolute;
    right: 55px;
    top: 50%;
    transform: translateY(-50%);
    pointer-events: none; /* Allows clicks to pass through to the box behind it */
}

</style>
""", unsafe_allow_html=True)

# This is page title visible in the browser tab #
st.set_page_config(
    page_title="My Doc Info Extractor"
) 

# This is the title part of the page which is in the main screen #
with st.container():
    st.title("Welcome to My Doc Info Extractor")
    #with st.popover("Click to view Citations"):
    #    st.write("Here are the sources:")

with st.container():
    if "messages" not in st.session_state:
            st.session_state.messages = []
            
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
user_input=st.chat_input(placeholder="Type a message... ", accept_file=True) 
if user_input:
# Handle the text part of the input
    user_text = user_input.text
    user_files=user_input.files
    if user_text:
        # Append user message to history
        st.session_state.messages.append({"role": "user", "content": user_text, "files": user_files})
        # Display the user message immediately
        with st.chat_message("user"):
            st.markdown(user_text)
            if user_files:
                for file in user_files:
                    st.markdown(f"Uploaded file: {file.name}")
        with st.chat_message("assistant"):
            with st.spinner("Thinking....."):
                response=client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=user_text,
                    )
                st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

# This is the bottom part  - the FOOTER #
with st.bottom:
    st.markdown("""<div style='text-align: center;'>Copyright © 2026 My Doc Info Extractor 
                made by <strong>VIVEK B SHAH</strong>. All rights reserved.</div>""",
                unsafe_allow_html=True) 