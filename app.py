import streamlit as st
from openai import OpenAI

# This is page title visible in the browser tab #
st.set_page_config(
    page_title="My Doc Info Extractor"
) 

def process_pdf(file):
    print("Processing PDF file:")
    pass

def process_docx(file):
    print("Processing DOCX file:")
    pass

client=OpenAI(
              api_key=st.secrets["GROQ_API_KEY"],
              base_url="https://api.groq.com/openai/v1"
             )
# for model in client.models.list():
#      print(f"Model ID: {model.name} -> Display: {model.display_name}")

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

    border: 2px solid var(--st-secondary-background-color);
    border-radius: 10px;
    padding: 8px 10px;

    background-color: var(--st-secondary-background-color);
    color: var(--st-text-color);

    white-space: pre-wrap;
}

/* Apply theme-aware text color inside user messages */
div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) p {
    color: var(--st-text-color);
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
            full_response = ""
            response_placeholder=st.empty()
            try:
                with st.spinner("Thinking....."):
                    response=client.chat.completions.create(
                        model="openai/gpt-oss-safeguard-20b",
                        messages=[{
                            "role":"system",
                            "content":("You are a helpful and factual AI assistant that answers questions in the shortest possible manner. "
                            "Provide accurate names, dates, and facts. "
                            "Never invent information or use placeholders "
                            "Use web search to verify factual information. "
                            "If something cannot be verified, say so."
                            )
                            },
                            {
                            "role": "user", "content": user_text
                            }],
                          tools=[{"type": "browser_search"}],
                          tool_choice="auto",
                          stream=False
                        )
                    # for chunk in response_stream:
                    #     if chunk.choices[0].delta.content:
                    #         full_response+=chunk.choices[0].delta.content
                    #         response_placeholder.markdown(full_response+" ")
                    full_response = response.choices[0].message.content or ""
                    response_placeholder.markdown(full_response)
                #st.markdown(response.text)
            except Exception as e:
                #st.error("An error occurred. Please try again later.", icon="🚨")
                st.exception(e)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        
# This is the bottom part  - the FOOTER #
with st.bottom:
    st.markdown("""<div style='text-align: center;'>Copyright © 2026 My Doc Info Extractor 
                made by <strong>VIVEK B SHAH</strong>. All rights reserved.</div>""",
                unsafe_allow_html=True) 