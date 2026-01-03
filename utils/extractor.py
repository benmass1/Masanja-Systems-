import pdfplumber

def extract_text_from_pdf(pdf_path):
    """
    Inasoma PDF na kutoa maandishi ukurasa kwa ukurasa
    """
    all_text = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text.append(text)
        return all_text
    except Exception as e:
        print(f"Hitilafu wakati wa kusoma PDF: {e}")
        return None
￼Enter
