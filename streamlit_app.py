import os
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = os.getenv("API_URL")

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Mind Map Generator API endpoint
mindmap_url = API_URL +  "/generate_mindmap"

# Header Section
st.title("Mind Map Generator with AI Assistance")
st.write(
    "Generate mind maps by describing your topic. This app uses the Gemini model to create a Markdown-based mind map "
    "description, which is then converted into an image."
)

# User Input Section
st.subheader("Step 1: Describe Your Mind Map Topic")
user_input = st.text_area(
    "Enter a topic or a detailed description of the mind map you want to create",
    height=200,
    placeholder="E.g., Climate Change, AI in Healthcare, etc."
)

# Gemini API Integration Section
if st.button("Generate Markdown from Gemini"):
    if user_input:
        try:
            gemini_prompt = f"Generate a mind map for the following topic in Markdown format only, use # to show hierarchy and only text, no special characters.\
            Make sure its not flat, it increases with each depth level. make it more long than wide, you can only double nodes each tree level : {user_input}"
            gemini_response = model.generate_content(gemini_prompt)
            markdown_text = gemini_response.text

            # Display Gemini's Markdown output
            st.subheader("Generated Markdown by Gemini")
            st.code(markdown_text, language="markdown")

            # Save the Markdown to session state for next step
            st.session_state["markdown_text"] = markdown_text

        except Exception as e:
            st.error(f"An error occurred with the Gemini API: {e}")
    else:
        st.warning("Please enter text to generate a mind map.")

# Mind Map Generation Section
if "markdown_text" in st.session_state:
    st.subheader("Step 2: Generate Mind Map Image")
    if st.button("Generate Mind Map Image"):
        payload = {"markdown_text": st.session_state["markdown_text"]}

        try:
            # Send Markdown text to the Mind Map API
            print("Sending request to Mind Map API", mindmap_url)
            response = requests.post(mindmap_url, json=payload)

            # Handle the response
            if response.status_code == 200:
                # Display the generated mind map image
                image = Image.open(BytesIO(response.content))
                # Display the generated mind map image, size adjusted to fit the screen atleast 600x600
                st.image(image, caption="Generated Mind Map")


            else:
                st.error(f"Failed to generate mind map. Status code: {response.status_code}")
                st.json(response.json())  # Show error details if available

        except requests.RequestException as e:
            st.error(f"An error occurred with the Mind Map API: {e}")

# Optional: Error Handling & Feedback
if st.session_state.get("markdown_text") is None and not user_input:
    st.info("Enter a description and click 'Generate Markdown from Gemini' to start.")