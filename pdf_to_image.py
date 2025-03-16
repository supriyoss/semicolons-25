from pdf2image import convert_from_path
from os import path, makedirs

def convert_pdf_to_images(pdf_path, output_folder, dpi=350, format='jpg'):
    """
       Convert a PDF file to images and save them to the specified folder.

       Parameters:
       - pdf_path: Path to the PDF file
       - output_folder: Directory to save the images
       - dpi: Image quality/resolution (default: 300)
       - format: Image format (default: png)

       Returns:
       - List of paths to the created images
       """
    # Create the output folder if it doesn't exist
    if not path.exists(output_folder):
        makedirs(output_folder)

    # Get the PDF filename without extension for naming the images
    pdf_filename = path.splitext(path.basename(pdf_path))[0]

    # Convert PDF to images
    images = convert_from_path(pdf_path, poppler_path=r"E:\Program Files\PyCharm 2023.1.3\Release-24.08.0-0\poppler-24.08.0\Library\bin")

    image_paths = []
    for i, image in enumerate(images):
        filename = f"{pdf_filename}_page_{i+1:03d}.{format}"
        image_path = path.join(output_folder, filename)

        image.save(image_path, "JPEG")
        image_paths.append(image_path)
        print(f"Saved:{image_path}")

    print(f"Converted {len(images)} pages from '{pdf_path}' to {format.upper()} images.")
    return image_paths

if __name__ == "__main__":

    pdf_file = r"E:\Semicolons\semicolons-25\sample-invoice.pdf"
    output_dir= r"E:\Semicolons\semicolons-25\coverted-images"

    convert_pdf_to_images(pdf_file, output_dir)