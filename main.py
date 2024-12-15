import openai
from openai import OpenAI, AsyncOpenAI
from PIL import Image
import os
from pdf2image import convert_from_path
import cv2
import numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY")


def API_call(prompt):
    response = openai.Completion.create(
        model="gpt-4o",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    answer = response.choices[0].text
    return answer

input_pdf = "C:/Users/abhay/OneDrive/Desktop/AT/Document-QA/gate_scorecard.pdf"


def pdf_to_image(pdf_path):
    """
    Converts a PDF file to an image format.

    Args:
        pdf_path (str): The path to the PDF file to be converted.

    Returns:
        An image or a list of images representing the pages of the PDF.
    """
    images = convert_from_path(pdf_path)
    images[0].save("pdf_image.jpg", "JPEG")


def enhance_image_quality(image_path):
    """
    Enhances the quality of an input image.

    Args:
        image_path (str): Path to the input image.

    Returns:
        numpy.ndarray: Enhanced image.
    """
    # Read the input image
    image = cv2.imread(image_path)

    # Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    # Apply histogram equalization to improve contrast
    lab_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_image)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    enhanced_image = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # Apply sharpening to improve details
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened_image = cv2.filter2D(enhanced_image, -1, kernel)
    cv2.imwrite("enhanced_image.jpg", sharpened_image)


pdf_to_image(pdf_path=input_pdf)
enhance_image_quality("pdf_image.jpg")

image = Image.open("enhanced_image.jpg")

user_query = "What is the name mentioned in the gate scorecard?"
prompt = f"""You are a smart document Question-Answering helper
           Your task is to answer the following question: {user_query}
           Use the image {image} to answer the question.
           If you dont find the answer. dont make assumptions about the answer, return gracefully that
           this information does not exist in the give document
           """

answer = API_call(prompt)
print(answer)

