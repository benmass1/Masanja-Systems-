from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from utils.extractor import extract_text_from_pdf
from utils.translator_core import translate_content
from utils.formatter import save_as_pdf

# Kuanzisha Flask na index.html ikiwa kwenye root
app = Flask(__name__, template_folder='.')

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Faili halijapatikana"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "Jina la faili ni tupu"}), 400

    # 1. Hifadhi PDF asilia
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # 2. Toa maandishi (Extraction)
    raw_text = extract_text_from_pdf(file_path)
    if not raw_text:
        return jsonify({"status": "error", "message": "Imeshindwa kusoma PDF"}), 500

    # 3. Tafsiri (Kwa majaribio: Tunatafsiri kurasa 3 za mwanzo)
    try:
        translated_pages = translate_content(raw_text[:3], target_lang='sw')
        full_translation = "\n\n".join(translated_pages)
        
        # 4. Tengeneza PDF Mpya ya Kiswahili
        output_filename = f"Masanja_Tafsiri_{file.filename}"
        save_as_pdf(full_translation, output_filename)
        
        return jsonify({
            "status": "success", 
            "message": "Tafsiri imekamilika!",
            "data": full_translation,
            "download_link": f"/download/{output_filename}"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    # Hii inaruhusu mtumiaji kupakua faili kutoka folda la processed
    return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

