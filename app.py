import streamlit as st
from document_processor import get_page_urls, get_url_content
from chatbot_engine import Chatbot
from utils import clean_text

# Set up the Streamlit page
st.set_page_config(page_title="AI Document Chatbot", layout="wide")
st.header("AI Document Chatbot")

# Input for the base URL or document link
base_url = st.text_input("Enter the URL of the site or PDF you're interested in:", "")

if base_url:
    # Fetch and process document contents from the given URL
    with st.spinner("Fetching and processing document(s)..."):
        urls = get_page_urls(base_url)
        if not urls:
            st.error("Failed to retrieve URLs. Please check the link and try again.")
        else:
            # Initialize the chatbot with documents from the URLs
            chatbot = Chatbot(urls)

            # Chat interface
            st.write("## Chat with AI")
            chat_container = st.empty()  # Container for dynamic chat updates
            user_input = st.text_input("Ask me anything about the documents:", key="user_input")

            if user_input:
                # Clean the user input before processing
                cleaned_input = clean_text(user_input)

                # Generate response from the chatbot
                with st.spinner("Thinking..."):
                    response = chatbot.get_response(cleaned_input)

                # Display the conversation
                chat_container.markdown(f"**You:** {user_input}")
                chat_container.markdown(f"**AI:** {response}")
else:
    st.write("Please enter a URL to begin.")

