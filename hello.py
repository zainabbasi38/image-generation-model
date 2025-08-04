from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Streamlit UI
st.set_page_config(page_title="Gemini Image Generator", layout="centered")
st.title("🎨 Gemini Image Generation Model")
st.markdown("Enter a prompt and generate an AI image using Google's Gemini model.")

# Input prompt
user_input = st.text_input("🖊️ What type of image do you want to generate?", placeholder="e.g., a futuristic city at night")

# Load Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY not found in .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

# Create a safe path for saving images

def generate_image(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(response_modalities=['TEXT', 'IMAGE'])
        )

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                # print(part.text)
                st.write(part.text)
            elif part.inline_data is not None:
                image = Image.open(BytesIO((part.inline_data.data)))
                image.save('gemini-native-image2.png')
                st.image("D:\image-generation-model\gemini-native-image2.png", caption="Generated Image")
                st.success("Image generated successfully.")
                # image.show()

    except Exception as e:
        st.error(f"⚠️ An error occurred: {str(e)}")

# Run the generation when prompt is given
if user_input:
    generate_image(user_input)
