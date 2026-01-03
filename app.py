
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from utils.extractor import extract_text_from_pdf
from utils.translator_core import translate_content
from utils.formatter import save_as_pdf

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
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Mchakato wa Masanja AI
    raw_text = extract_text_from_pdf(file_path)
    translated_pages = translate_content(raw_text[:5], target_lang='sw') # Kurasa 5 za kwanza
    full_text = "\n\n".join(translated_pages)

    # Tengeneza PDF mpya
    output_name = f"Tafsiri_{file.filename}"
    save_as_pdf(full_text, output_name)

    return jsonify({
        "status": "success", 
        "data": full_text,
        "download_link": f"/download/{output_name}"
    })

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
