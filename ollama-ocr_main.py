import fitz  # PyMuPDF
import os
from ollama_ocr import OCRProcessor  # Ensure ollama-ocr is installed

print("fitz is loaded from:", fitz.__file__)
print("Available attributes in fitz:", dir(fitz))

def extract_pdf_page_as_image(pdf_path, output_filename="extracted_page.jpg"):
    """
    Opens the PDF at pdf_path, prompts the user for a page number (1-indexed),
    extracts that page as an image, and saves it as a JPEG file.
    Returns the path to the saved image.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return None

    total_pages = doc.page_count
    print(f"The PDF has {total_pages} page(s).")

    # Prompt user for the page number
    try:
        page_num = int(input("Enter the page number to process for OCR (1-indexed): "))
    except ValueError:
        print("Invalid input. Please enter a numeric page number.")
        return None

    if page_num < 1 or page_num > total_pages:
        print("Page number is out of range.")
        return None

    # Extract the specified page 
    page = doc[page_num - 1]
    pix = page.get_pixmap()

    output_dir = os.path.dirname(output_filename)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        pix.save(output_filename)
        print(f"Page {page_num} has been saved as {output_filename}")
    except Exception as e:
        print(f"Error saving image: {e}")
        return None

    return output_filename

if __name__ == '__main__':
    pdf_path = "american_homes_4_rent_2024.pdf"
    
    image_path = extract_pdf_page_as_image(pdf_path)
    if image_path:
        print("Image is ready for OCR processing.")

        # Initialize the OCR processor with the desired model.
        ocr = OCRProcessor(model_name='llama3.2-vision:11b')
        
        # Optionally, define a custom prompt if needed.
        custom_prompt = (
            "Extract all text from the image, preserving the layout if possible."
        )
        
        # Process the image for OCR.
        try:
            ocr_result = ocr.process_image(
                image_path=image_path,
                format_type="text",  # Options: text, markdown, json, etc.
                custom_prompt=custom_prompt
            )
            print("OCR Result:")
            print(ocr_result)
        except Exception as e:
            print(f"Error during OCR processing: {e}")
