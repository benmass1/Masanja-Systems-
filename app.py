
from flask import Flask, render_template, request, jsonify
import os

# MUHIMU: template_folder='.' inaruhusu index.html kukaa kwenye root
app = Flask(__name__, template_folder='.')

# Folda za kuhifadhi vitabu
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    # Flask sasa itatafuta index.html hapo hapo kwenye Masanja_Systems/
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Hakuna faili lililochaguliwa"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "Jina la faili ni tupu"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    return jsonify({
        "status": "success", 
        "message": f"Masanja Systems imepokea: {file.filename}"
    })

if __name__ == '__main__':
    # Hii inaruhusu ku-run kwenye simu yako
    app.run(host='0.0.0.0', port=5000, debug=True)
