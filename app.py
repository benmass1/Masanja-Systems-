from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from utils.extractor import extract_text_from_pdf
from utils.translator_core import translate_content
from utils.formatter import save_as_pdf

# 1. Muhimu: template_folder='.' kwa sababu index.html ipo kwenye root
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
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        raw_text = extract_text_from_pdf(file_path)
        translated_pages = translate_content(raw_text[:3], target_lang='sw')
        full_translation = "\n\n".join(translated_pages)
        output_name = f"Masanja_Tafsiri_{file.filename}"
        save_as_pdf(full_translation, output_name)
        
        return jsonify({
            "status": "success", 
            "data": full_translation,
            "download_link": f"/download/{output_name}"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)

# 2. Muhimu: Port ya Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

