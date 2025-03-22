import pytesseract
from pdf2image import convert_from_path
from vector_db import save_text_embedding


def process_pdf_file(pdf_path):
    """Extract text from each PDF page and save embeddings separately."""
    print(f"Processing PDF: {pdf_path}")
    try:
        images = convert_from_path(pdf_path)

        for page_num, image in enumerate(images, start=1):
            extracted_text = pytesseract.image_to_string(image)

            if extracted_text.strip():
                unique_id = f"{pdf_path}_page_{page_num}"
                save_text_embedding(unique_id, extracted_text)
                print(f"OCR and embedding saved for: {pdf_path}, Page {page_num}")
            else:
                print(f"Skipped empty page {page_num} of {pdf_path}")

    except Exception as e:
        print(f"Error processing PDF: {e}")