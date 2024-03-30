import fitz  # PyMuPDF
import google.generativeai as genai

import os
from dotenv import load_dotenv
load_dotenv()


if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY not found in environment or .env file")

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Set up the model
vision_generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

vision_model = genai.GenerativeModel(
    model_name="gemini-1.0-pro-vision-latest",
    generation_config=vision_generation_config,
    safety_settings=safety_settings,
)

def read_text_from_pdf(pdf_path):
    text = ""
    pdf_document = fitz.open(pdf_path)
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        text += page.get_text()
    return text

def read_text_from_image(file):
    
    image_data = file.read()
    
    image_parts = [
        {"mime_type": "image/jpeg", "data": image_data},
    ]
    
    prompt = [
        """
        Read all the text from the image provided and return it as a string.
        It should be readable by a human.
        If "\n" is present, replace it by creating a new line.
        If "\t" is present, replace it by creating a tab.
        """,
        image_parts[0],
    ]
    
    response = vision_model.generate_content(prompt)
    print(response.text)
    
    return response.text

# Example usage
# pdf_path = "example.pdf"  # Path to your PDF file
# image_path = "example.png"  # Path to your image file

# Reading text from PDF
# pdf_text = read_text_from_pdf(pdf_path)
# print("Text from PDF:")
# print(pdf_text)

# # Reading text from image
# image_text = read_text_from_image(image_path)
# print("\nText from image:")
# print(image_text)
