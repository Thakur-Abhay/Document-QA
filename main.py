import openai
from openai import OpenAI, AsyncOpenAI
from PIL import Image
import os
from .context_enricher import GenericEnrichmentEngine

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


preprocesser_obj = GenericEnrichmentEngine()
input_pdf = "C:/Users/abhay/OneDrive/Desktop/AT/Document-QA/gate_scorecard.pdf"
preprocesser_obj.pdf_to_image(input_pdf)
preprocesser_obj.enhance_image_quality("pdf_image.jpg")
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

