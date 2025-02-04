from flask import Flask, request, send_file, jsonify
from fpdf import FPDF
from docx import Document
import os

# ✅ Définition correcte de l'application Flask
app = Flask(__name__)

# ✅ Route pour vérifier que le serveur fonctionne
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Le serveur fonctionne ! Utilisez /generate-document pour créer un fichier."})

# ✅ Route pour générer un document
@app.route("/generate-document", methods=["POST"])
def generate_document():
    try:
        if not request.is_json:
            return jsonify({"error": "Requête invalide, envoyez des données JSON"}), 400

        data = request.json
        doc_type = data.get("type")
        content = data.get("content", "Document généré par le chatbot.")

        if not doc_type or not isinstance(content, str):
            return jsonify({"error": "Paramètres invalides"}), 400

        file_path = ""

        if doc_type.lower() == "pdf":
            file_path = "document.pdf"
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)  # ✅ Police par défaut
            pdf.multi_cell(200, 10, content)
            pdf.output(file_path)

        elif doc_type.lower() == "word":
            file_path = "document.docx"
            doc = Document()
            doc.add_paragraph(content)
            doc.save(file_path)

        else:
            return jsonify({"error": "Type de document non supporté, utilisez 'pdf' ou 'word'"}), 400

        if not os.path.exists(file_path):
            return jsonify({"error": "Erreur lors de la génération du fichier"}), 500

        response = send_file(file_path, as_attachment=True)
        os.remove(file_path)
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Vérification des routes disponibles
print(app.url_map)

# ✅ Configuration du port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Utilisation du port de Render
    app.run(host="0.0.0.0", port=port, debug=True)
