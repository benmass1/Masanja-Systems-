
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
# Hakikisha mafaili haya yapo ndani ya folder la utils
from utils.extractor import extract_text_from_pdf
from utils.translator_core import translate_content
from utils.formatter import save_as_pdf

# 1. Hapa tunaiambia Python kuwa index.html ipo kwenye Root Directory (.)
app = Flask(__name__, template_folder='.')

# Sehemu ya kuhifadhi mafaili
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def home():
    # Itatafuta index.html kwenye root ya Masanja_Systems
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Faili halijapatikana"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "Jina la faili ni tupu"}), 400

    # Hifadhi faili lililopakiwa
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        # 1. Toa maandishi kwenye PDF
        raw_text = extract_text_from_pdf(file_path)
        if not raw_text:
            return jsonify({"status": "error", "message": "PDF haina maandishi yanayosomeka"}), 400

        # 2. Tafsiri maandishi (Kwa majaribio: Kurasa 3 za mwanzo)
        translated_pages = translate_content(raw_text[:3], target_lang='sw')
        full_translation = "\n\n".join(translated_pages)
        
        # 3. Tengeneza PDF mpya ya Kiswahili
        output_name = f"Masanja_Tafsiri_{file.filename}"
        save_as_pdf(full_translation, output_name)
        
        # Tuma majibu ya mafanikio na link ya kudownload
        return jsonify({
            "status": "success", 
            "message": "Tafsiri imekamilika!",
            "data": full_translation,
            "download_link": f"/download/{output_name}"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    # Inaruhusu kupakua faili kutoka folder la processed
    return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)

# 2. SEHEMU MUHIMU KWA AJILI YA RENDER (Port Configuration)
if __name__ == '__main__':
    # Render itatoa PORT namba, kama haipo itatumia 5000
    port = int(os.environ.get("PORT", 5000))
    # Host lazima iwe 0.0.0.0 ili ionekane mtandaoni
    app.run(host='0.0.0.0', port=port)
