@app.route("/generate-document", methods=["POST"])
def generate_document():
    try:
        if not request.is_json:
            return jsonify({"error": "Requête invalide, envoyez des données JSON"}), 400
        
        data = request.json
        print("Données reçues:", data)  # Ajout pour voir les données reçues

        doc_type = data.get("type")
        content = data.get("content", "Document généré par le chatbot.")

        if not doc_type or not isinstance(content, str):
            return jsonify({"error": "Paramètres invalides"}), 400

        file_path = ""

        if doc_type.lower() == "pdf":
            file_path = "document.pdf"
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)
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
        print("Erreur serveur:", str(e))  # Ajout pour voir l'erreur
        return jsonify({"error": str(e)}), 500
