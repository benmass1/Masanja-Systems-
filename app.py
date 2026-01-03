from flask import Flask, render_template, request, jsonify
import os
from utils.extractor import extract_text_from_pdf
from utils.translator_core import translate_content

app = Flask(__name__, template_folder='.')

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
        return jsonify({"status": "error", "message": "Imeshindwa kusoma PDF hii"}), 500

    # 3. Tafsiri (Translation) - Tunatafsiri kurasa 2 za mwanzo kama jaribio
    # Unaweza kuongeza kurasa zote baadaye
    try:
        translated_pages = translate_content(raw_text[:2], target_lang='sw')
        full_translation = "\n\n".join(translated_pages)
        
        return jsonify({
            "status": "success", 
            "message": "Tafsiri imekamilika!",
            "data": full_translation
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

