# routes/carte_routes.py
import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from models.carte import Carte
from models import db

carte_bp = Blueprint('carte_bp', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@carte_bp.route('/upload-carte', methods=['POST'])
def upload_carte():
    # Vérifier que le fichier est présent dans la requête
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nom de fichier vide'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        # Créer le dossier si nécessaire
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # Enregistrer le chemin dans la base de données
        carte = Carte(chemin=file_path)
        db.session.add(carte)
        db.session.commit()

        return jsonify({'message': 'Fichier uploadé avec succès', 'chemin': file_path}), 200

    return jsonify({'error': 'Extension de fichier non autorisée'}), 400

@carte_bp.route('/download-carte/<int:carte_id>', methods=['GET'])
def download_carte(carte_id):
    # Récupérer l'enregistrement correspondant à la carte
    carte = Carte.query.get(carte_id)
    if not carte:
        return jsonify({'error': 'Carte non trouvée'}), 404

    # Extraire le nom du fichier à partir du chemin stocké
    filename = os.path.basename(carte.chemin)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
