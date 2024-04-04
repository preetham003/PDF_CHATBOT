import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    text = ''
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Iterate through each page
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document[page_number]

        # Extract text from the page
        text += page.get_text()

    # Close the PDF document
    pdf_document.close()

    return text

# Print the extracted text
# print(extracted_text)
def justify_text(paragraph, line_width):
    words = paragraph.split()
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        if current_width + len(word) <= line_width:
            current_line.append(word)
            current_width += len(word) + 1  # Include space after word
        else:
            lines.append(current_line)
            current_line = [word]
            current_width = len(word) + 1  # Include space after word

    if current_line:
        lines.append(current_line)

    justified_lines = []
    for line in lines:
        if len(line) > 1:
            total_spaces_needed = line_width - sum(len(word) for word in line)
            space_gaps = len(line) - 1
            spaces_per_gap = total_spaces_needed // space_gaps
            extra_spaces = total_spaces_needed % space_gaps

            justified_line = ''
            for i, word in enumerate(line):
                justified_line += word
                if i < space_gaps:
                    justified_line += ' ' * (spaces_per_gap + (i < extra_spaces))
            justified_lines.append(justified_line)
        else:
            justified_lines.append(line[0])

    return '\n'.join(justified_lines)

def single_line_text(paragraph):
    # Remove line breaks and extra spaces
    single_line = ' '.join(paragraph.split())
    return single_line

pdf_files = ['fess1ps.pdf', 'fess101.pdf','fess102.pdf', 'fess103.pdf', 'fess104.pdf','fess105.pdf']

text=''
# Iterate through each PDF file and extract text
for pdf_file_path in pdf_files:
    extracted_text = extract_text_from_pdf(pdf_file_path)
    justified_paragraph = single_line_text(extracted_text)
    text+=justified_paragraph
    print(justified_paragraph)
    print('-' * 80) 
# Example usage
line_width = 80
justified_paragraph = single_line_text(extracted_text)
print(justified_paragraph)
