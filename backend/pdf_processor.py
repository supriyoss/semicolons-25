import pytesseract
from pdf2image import convert_from_path
from vector_db import save_text_embedding


def process_pdf_file(pdf_path):
    print(f"Processing PDF: {pdf_path}")

    try:
        images = convert_from_path(pdf_path)
        extracted_text = ""

        for i, image in enumerate(images):
            page_text = pytesseract.image_to_string(image)
            extracted_text += f"Page {i + 1}:\n{page_text}\n{'-' * 40}\n"

        # Save OCR result and embedding to Pinecone
        save_text_embedding(pdf_path, extracted_text)
        print(f"OCR and embedding saved for: {pdf_path}")

    except Exception as e:
        print(f"Error processing PDF: {e}")
