import fitz  # PyMuPDF
from PIL import Image

def extract_text_with_ocr(pdf_path):
  """
  Extracts text from a PDF, including text within images using Tesseract OCR.

  Args:
      pdf_path: Path to the PDF file.

  Returns:
      A list containing the extracted text from each page and any extracted text from images.
  """
  doc = fitz.open(pdf_path)
  extracted_text = []
  print(type(doc))
  c=0
  for page in doc:
    if c<5:
        page_text = page.get_text("text")  # Extract text blocks
        extracted_text.append(page_text)
        print("txt"*5,extracted_text)
        # Extract images from the page
        for image in page.get_images():
        # Get image data (x0, y0, x1, y1) and extract the image
            if isinstance(image, list):
                x0, y0, x1, y2 = image[0]
                image_data = page.get_pixmap_matrix(image[0])
            else:
                print(f"Warning: Unexpected image format on page {page.number + 1}. Skipping image extraction.")
                continue
            # Convert image data to PIL Image format
            pil_image = Image.fromarray(image_data, mode="RGB")
            print(type(pil_image))
            # Use Tesseract OCR to extract text from the image
            try:
                import pytesseract
                image_text = pytesseract.image_to_string(pil_image)
                extracted_text.append(f"Image Text (Page {page.number + 1}):\n{image_text}")
            except ImportError:
                print("Warning: Tesseract OCR not installed. Image text extraction skipped.")
        c+=1
  doc.close()
  return extracted_text

# Example usage
pdf_path = "icrc_battle_villages.pdf"  # Replace with your actual PDF path
extracted_text = extract_text_with_ocr(pdf_path)

for page_text in extracted_text:
  print(page_text)
  print("=" * 20)
