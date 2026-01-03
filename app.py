herefrom flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Pakia siri kutoka kwenye .env kama zipo
load_dotenv()

app = Flask(__name__)

# Mpangilio wa Folda
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Hakikisha folda muhimu zipo
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # Hapa tunaiambia Flask ikachukue ile UI kule kwenye templates
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Hakuna faili lililopatikana"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "Jina la faili ni tupu"}), 400

    # Hifadhi faili la mteja
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    return jsonify({
        "status": "success", 
        "message": f"Kitabu '{file.filename}' kimepokelewa na Masanja Systems!"
    })

if __name__ == '__main__':
    # Tunatumia port 5000 ambayo ni standard kwa Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
