# routes/site_carte.py
from flask import Blueprint, request, jsonify, current_app
from flasgger import swag_from
from models.site import Site
from models.carte import Carte
from models import db

site_carte_bp = Blueprint('site_carte_bp', __name__)

@site_carte_bp.route('/<int:site_id>/assign', methods=['POST'])
@swag_from({
    'tags': ['Site Carte'],
    'description': "Assigne une carte existante à un site. Le JSON doit contenir 'card_id'.",
    'consumes': ['application/json'],
    'parameters': [
        {
            'name': 'site_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': "ID du site"
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'card_id': {'type': 'integer', 'example': 5}
                },
                'required': ['card_id']
            }
        }
    ],
    'responses': {
        200: {
            'description': "Carte assignée au site avec succès.",
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': "Carte assignée au site avec succès."}
                }
            }
        },
        400: {'description': "Carte déjà assignée ou champ manquant."},
        404: {'description': "Site ou carte non trouvé."},
        500: {'description': "Erreur interne."}
    }
})
def assign_card_to_site(site_id):
    try:
        site = Site.query.get(site_id)
        if not site:
            return jsonify({'error': 'Site non trouvé'}), 404

        data = request.get_json()
        if not data or 'card_id' not in data:
            return jsonify({'error': 'Le champ "card_id" est requis'}), 400

        card_id = data['card_id']
        card = Carte.query.get(card_id)
        if not card:
            return jsonify({'error': 'Carte non trouvée'}), 404

        # Vérifier si la carte est déjà attribuée (à un étage ou à un site)
        if card.etage_id is not None or card.site_id is not None:
            return jsonify({'error': 'Carte déjà assignée à un étage ou un site'}), 400

        card.site_id = site.id
        db.session.commit()
        return jsonify({'message': "Carte assignée au site avec succès."}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in assign_card_to_site: {e}")
        return jsonify({'error': str(e)}), 500
