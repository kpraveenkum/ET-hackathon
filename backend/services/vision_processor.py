import fitz
from pathlib import Path


def pdf_to_images(pdf_path):

    output_dir = Path("uploads/images")

    output_dir.mkdir(
        exist_ok=True
    )


    doc = fitz.open(pdf_path)

    images = []


    for index, page in enumerate(doc):

        pix = page.get_pixmap(
            dpi=200
        )


        image_path = (
            output_dir /
            f"page_{index+1}.png"
        )


        pix.save(
            str(image_path)
        )


        images.append(
            str(image_path)
        )


    return images