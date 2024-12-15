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


    async def pdf_parser(self, pdf_path):
        pass
