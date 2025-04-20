import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def gemini_response(input_text, image=None, prompt=None):
    """Function to get response from Gemini API."""
    if image and prompt:
        response = model.generate_content([input_text, image[0], prompt])
    elif input_text:
        response = model.generate_content([input_text])
    else:
        response = model.generate_content([input_text])
    return response.text

def input_image_details(uploaded_file):
    """Handles image uploads and returns processed image data."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit UI Configuration
st.set_page_config(page_title="HealthSphere", layout="wide")
st.title("🩺 HealthSphere - Your Medical Companion")
st.markdown("""
    <style>
    body {background-color: #f5f5f5;}
    .stApp {background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1);}
    </style>
    """, unsafe_allow_html=True)

# Sidebar for Navigation
mode = st.sidebar.radio("Choose Mode", ("📄 Medical Report Analysis", "💬 Mental Health Chatbot"))

# Medical Report Analysis Mode
if mode == "📄 Medical Report Analysis":
    st.subheader("Upload and Analyze Medical Reports")
    user_input = st.text_input("Enter your query about the report:")
    uploaded_file = st.file_uploader("Upload Medical Report (JPG, PNG):", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Medical Report", use_container_width=True)
    
    submit = st.button("Analyze Report")

    input_prompts = """Analyze the attached image of the medical report/blood test report.
    Give me correct answers based on my questions from the image. Provide health advice if asked."""
    
    if submit:
        try:
            image_data = input_image_details(uploaded_file)
            response = gemini_response(user_input, image_data, input_prompts)
            st.subheader("Analysis Result")
            st.write(response)
        except FileNotFoundError as e:
            st.error(f"Error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# Mental Health Chatbot Mode
elif mode == "💬 Mental Health Chatbot":
    st.subheader("Mental Health Chatbot - Chat Freely")
    st.markdown("Ask any mental health-related questions, and I'll respond empathetically.")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    chatbot_input = st.chat_input("Type your message here...")

    if chatbot_input:
        st.session_state.chat_history.append({"role": "user", "content": chatbot_input})
        chatbot_response = gemini_response(chatbot_input)
        st.session_state.chat_history.append({"role": "assistant", "content": chatbot_response})
        with st.chat_message("assistant"):
            st.markdown(chatbot_response)

# Footer
st.markdown("---")
st.markdown("Developed by -  Kritika Kashyap (1OX21AI014), Swathi S (1OX21AI041), Naveen N (1OX21AI023)")
