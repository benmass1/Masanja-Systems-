from fpdf import FPDF
import os

def save_as_pdf(translated_text, output_filename):
    """
    Inachukua maandishi na kutengeneza faili la PDF
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Tunatumia font ya kimsingi (Arial)
    pdf.set_font("Arial", size=12)
    
    # Kuandika maandishi kwenye PDF
    # Kumbuka: .encode('latin-1', 'ignore').decode('latin-1') inasaidia kuzuia error za herufi geni
    clean_text = translated_text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    
    # Hifadhi faili kwenye folda la processed
    output_path = os.path.join('processed', output_filename)
    pdf.output(output_path)
    return output_path
￼Enter
