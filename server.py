import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Initialisation de l'application Flask
app = Flask(__name__)

# 🔹 Activer le logging pour Render et le debug
logging.basicConfig(level=logging.DEBUG)

# 🚀 Vérification que Render charge bien ce fichier
print("🚀 Le serveur Flask démarre sur Render !")

@app.before_request
def log_request_info():
    """Log des requêtes reçues pour faciliter le debug."""
    logging.info(f"📩 Méthode: {request.method} | URL: {request.url}")
    logging.info(f"📩 Headers: {request.headers}")
    logging.info(f"📩 Body: {request.get_data().decode('utf-8', errors='ignore')}")  # Affichage brut du body

CORS(app)  # Activer CORS pour autoriser les requêtes externes

# 📁 Dossier pour stocker les documents générés
UPLOAD_FOLDER = 'generated_documents'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Affichage de toutes les routes disponibles pour vérifier le bon fonctionnement sur Render
print("📌 Routes enregistrées sur le serveur Flask :")
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint} -> {rule.rule} -> {rule.methods}")

@app.route('/', methods=['GET'])
def home():
    """Endpoint de test pour vérifier si le serveur est actif."""
    return jsonify({"message": "Le serveur fonctionne ! Utilisez /generate-document pour créer un fichier."})

@app.route('/generate-document', methods=['POST', 'OPTIONS'])
def generate_document():
    """Endpoint pour générer un document texte à partir d'un JSON."""
    if request.method == 'OPTIONS':
        return '', 200  # Réponse rapide pour CORS

    try:
        # 🔹 Ajout de logs pour voir ce que Postman envoie
        logging.info("📩 Requête reçue : %s", request.data.decode('utf-8', errors='ignore'))
        logging.info("📩 Headers reçus : %s", request.headers)

        # 🔹 Vérifie si la requête contient bien du JSON
        data = request.get_json(force=True, silent=True)  # Force JSON parsing et ignore erreurs silencieusement

        if data is None:
            logging.error("🚨 Erreur : JSON mal formé ou manquant")
            return jsonify({"error": "Le contenu doit être au format JSON"}), 400

        # Vérifie si "content" est bien présent
        if "content" not in data:
            logging.error("🚨 Erreur : Champ 'content' manquant")
            return jsonify({"error": "Champ 'content' manquant"}), 400

        # Création du fichier texte avec le contenu reçu
        filename = "document_test.txt"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(data["content"])

        logging.info(f"✅ Document enregistré avec succès sous {filename}")
        return jsonify({
            "message": "Document généré avec succès",
            "filename": filename
        }), 200

    except Exception as e:
        logging.error(f"🚨 Exception : {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/static/<filename>', methods=['GET'])
def serve_document(filename):
    """Permet de télécharger un fichier généré."""
    return send_from_directory(UPLOAD_FOLDER, filename)

# Configuration pour Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Prendre le port de Render
    app.run(host='0.0.0.0', port=port, debug=True)
