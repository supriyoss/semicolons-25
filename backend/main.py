"""
Steps:
1. Input Documents(Shared Storage to be decided)
2. Check whether the document is pdf or image
3a. If image proceed to 4.
3b. If pdf, convert to image
4. Mark regions of image for information extraction
5. Apply OCR to the image
6. Send formatted data to the DB(DB yet to be decided)

"""
from pdf_to_image import convert_pdf_to_images

if __name__ == "__main__":
    
