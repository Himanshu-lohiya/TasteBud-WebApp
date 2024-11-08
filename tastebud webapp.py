from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

# Part 1: Importing Libraries
import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import os
from io import BytesIO

# Set the environment variable
os.environ['GOOGLE_API_KEY'] = "AIzaSyAl9pyuL8UPobF7zNnKpg-ZG9HTZJKYaTo"
genai.configure(api_key="AIzaSyAl9pyuL8UPobF7zNnKpg-ZG9HTZJKYaTo")
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
load_dotenv()  
# Load environment variables from .env file
api_key = os.getenv("AIzaSyAl9pyuL8UPobF7zNnKpg-ZG9HTZJKYaTo")  # Retrieve the API key
genai.configure(api_key=api_key)  # Configure the API with the key
## Function to load Google Gemini Pro Vision API And get response

# Part 5: Getting Response from the Gemini API
def get_gemini_response(input_prompt, image,input):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')  # Initialize the model
    response = model.generate_content([input_prompt, image[0]])  # Generate content
    return response

# Part 3: Loading the Image
def load_image(image_path):
    try:
        image = Image.open(image_path)  # Open the image file
        return image
    except Exception as e:
        print(f"Error loading image: {e}")  # Handle errors
        return None

# Part 4: Setting Up the Input Image
def input_image_setup(image_path):
    image = load_image(image_path)  # Load the image
    if image is not None:
        buffered = BytesIO()
        image.save(buffered, format="JPEG")  # Save the image to a BytesIO object
        bytes_data = buffered.getvalue()  # Get the byte data
        image_parts = [{
            "mime_type": "image/jpeg",  # Adjust based on the image type
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("Image could not be loaded")  # Raise error if image is not found
    
##initialize our streamlit app

st.set_page_config(page_title="TasteBud App")

st.header("TasteBud App")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Proceed")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----


"""

## If submit button is clicked

if submit:
    # Set up the image data from the uploaded file
    image_data = input_image_setup(uploaded_file)
    
    # Get the response from the Gemini model using the input prompt and image data
    response = get_gemini_response(input_prompt, image_data, input_prompt)
    
    # Convert the response to a dictionary
    response_dict = response.to_dict()  # Only if `response` is an object and not a dictionary
    
    # Extract the "text" part
    text_output = response_dict["candidates"][0]["content"]["parts"][0]["text"]
    
    # Display the extracted text in the Streamlit app
    st.subheader("The Response is")
    st.write(text_output)


