import fitz
import pytesseract
from PIL import Image


def extract_drawing_text(path):

    doc = fitz.open(path)

    extracted_text = ""


    for page in doc:

        pix = page.get_pixmap()

        image = Image.frombytes(
            "RGB",
            [
                pix.width,
                pix.height
            ],
            pix.samples
        )


        text = pytesseract.image_to_string(image)

        extracted_text += text


    return extracted_text
