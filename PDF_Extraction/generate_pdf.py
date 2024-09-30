from fpdf import FPDF

def generate_text_pdf(translated_docs, FONT_SIZE = 8, FONT_STYLE = "Arial", MARGIN = 10, LINE_SPACE = 5, PDF_NAME = "generated_pdf.pdf"):
    # Create a PDF object
    pdf = FPDF(orientation='P', unit='mm', format='A4') # P:portrait, L:Landscape, 'mm': Millimeters (default), 'pt': Points (1 point = 1/72 of an inch), 'cm': Centimeters, 'in': Inches
    pdf.set_auto_page_break(auto=True, margin=MARGIN)
    pdf.set_font(FONT_STYLE, size=FONT_SIZE)

    # Loop through each Document object and add its content to a new page
    for doc in translated_docs:
        pdf.add_page()
        pdf.multi_cell(0, LINE_SPACE, doc.encode('latin-1', 'replace').decode('latin-1'))  # Encode with 'replace' to handle unsupported chars

    # Save the PDF file
    pdf_filename = PDF_NAME
    pdf.output(pdf_filename)

    print(f"PDF '{pdf_filename}' created successfully.")