from pdf2image import convert_from_path
import cv2
import numpy as np


class GenericEnrichmentEngine:
    def __init__(self):
        pass

    async def pdf_to_image(self, pdf_path):
        """
        Converts a PDF file to an image format.

        Args:
            pdf_path (str): The path to the PDF file to be converted.

        Returns:
            An image or a list of images representing the pages of the PDF.
        """
        images = convert_from_path(pdf_path)
        images[0].save("pdf_image.jpg", "JPEG")

    async def enhance_image_quality(image_path):
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

    async def pdf_parser(self, pdf_path):
        pass
