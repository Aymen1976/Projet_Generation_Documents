from flask import Flask, request, jsonify, send_file
import subprocess
import os
import json

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Aucune donnée reçue"}), 400

    temp_file = 'sample_input_temp.json'
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    try:
        subprocess.run(['python', 'generate_document.py', temp_file], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    output_file = "document_chatbot.pdf" if data.get("format", "DOCX").upper() == "PDF" else "document_chatbot.docx"
    output_path = os.path.join(desktop_path, output_file)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
