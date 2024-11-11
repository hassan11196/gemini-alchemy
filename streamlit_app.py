import os
import streamlit as st
import requests
from dotenv import load_dotenv
import json
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = os.getenv("API_URL")

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Mind Map Generator API endpoint
mindmap_url = API_URL + "/generate_mindmap"

# Header Section
st.title("Mind Map Generator with AI Assistance")
st.write(
    "Generate mind maps by describing your topic. This app uses the Gemini model to create a Markdown-based mind map "
    "description, which is then converted into a dynamic mind map visualization."
)

# User Input Section
st.subheader("Step 1: Describe Your Mind Map Topic")

# Set default value if not already in session state
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""
if "tree_depth" not in st.session_state:
    st.session_state["tree_depth"] = 3

# Use session state to retain user input and tree depth
user_input = st.text_area(
    "Enter a topic or a detailed description of the mind map you want to create",
    value=st.session_state["user_input"],
    height=200,
    placeholder="E.g., Factors affecting Climate Change, AI in Healthcare, Advantages of Mindmapping, etc."
)
tree_depth = st.slider(
    "Select the maximum depth of the mindmap tree",
    1, 5, st.session_state["tree_depth"]
)

# Store values in session state
st.session_state["user_input"] = user_input
st.session_state["tree_depth"] = tree_depth

# Gemini API Integration Section
if st.button("Generate Markdown from Gemini"):
    if user_input:
        try:
            gemini_prompt = f"Generate a mind map for the following topic in Markdown format only, use # and then - to show hierarchy and only text, no special characters.\
            Make sure it's not flat, it increases with each depth level. Make it more long than wide; you can only double nodes each tree level, and maximum depth of tree should be {tree_depth}. Here's topic details for mindmap: {user_input}"
            gemini_response = model.generate_content(gemini_prompt)
            markdown_text = gemini_response.text

            # Display Gemini's Markdown output
            st.subheader("Generated Markdown by Google Gemini")
            st.code(markdown_text, language="markdown")

            # Save the Markdown to session state for next step
            st.session_state["markdown_text"] = markdown_text

        except Exception as e:
            st.error(f"An error occurred with the Gemini API: {e}")
    else:
        st.warning("Please enter text to generate a mind map.")

# Mind Map Generation Section
if "markdown_text" in st.session_state:
    st.subheader("Step 2: View Mind Map")
    # Display Markdown output again
    st.code(st.session_state["markdown_text"], language="markdown")

    if st.button("Generate Mind Map"):
        payload = {"markdown_text": st.session_state["markdown_text"]}

        try:
            # Send Markdown text to the Mind Map API
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                mindmap_url, data=json.dumps(payload), headers=headers
            )

            # Handle the response
            if response.status_code == 200:
                # Render the HTML returned from the API
                st.components.v1.html(response.text, height=600)
            else:
                st.error(f"Failed to generate mind map. Status code: {
                         response.status_code}")
                st.json(response.json())  # Show error details if available

        except requests.RequestException as e:
            st.error(f"An error occurred with the Mind Map API: {e}")

# Optional: Error Handling & Feedback
if st.session_state.get("markdown_text") is None and not user_input:
    st.info("Enter a description and click 'Generate Markdown from Gemini' to start.")
