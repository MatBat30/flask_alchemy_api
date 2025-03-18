# swagger.py
from flask import Blueprint, jsonify, current_app, request, send_from_directory
from flasgger import swag_from
from sqlalchemy import text
import os

from models import db
from models.site import Site
from models.batiment import Batiment
from models.etage import Etage
from models.BAES import BAES
from models.historique_erreur import HistoriqueErreur
from models.user import User
from models.role import Role

swagger_bp = Blueprint('swagger', __name__)

###############################
# Endpoints de tests "généraux"
###############################

@swagger_bp.route('/test-connection', methods=['GET'])
@swag_from({
    'tags': ['Database Tests'],
    'description': 'Teste la connexion à la base de données via une requête simple SELECT 1.',
    'responses': {
        200: {
            'description': 'Connexion réussie, retourne le résultat de SELECT 1.',
            'schema': {
                'type': 'object',
                'properties': {
                    'result': {'type': 'integer', 'example': 1}
                }
            }
        },
        500: {'description': 'Erreur lors de la connexion à la base de données.'}
    }
})
def test_connection():
    try:
        result = db.session.execute("SELECT 1")
        value = result.scalar()
        return jsonify({'result': value})
    except Exception as e:
        current_app.logger.error(f"Error in test_connection: {e}")
        return jsonify({'error': str(e)}), 500

@swagger_bp.route('/test-creation', methods=['GET'])
@swag_from({
    'tags': ['Database Tests'],
    'description': "Teste la création (ou l'existence) des tables en comptant les enregistrements dans certaines tables.",
    'responses': {
        200: {
            'description': "Retourne le nombre d'enregistrements dans les tables users, roles et dans la table d'association user_roles.",
            'schema': {
                'type': 'object',
                'properties': {
                    'users_count': {'type': 'integer', 'example': 0},
                    'roles_count': {'type': 'integer', 'example': 0},
                    'user_roles_count': {'type': 'integer', 'example': 0}
                }
            }
        },
        500: {'description': "Erreur lors du test de création des tables."}
    }
})
def test_creation():
    try:
        users_count = User.query.count()
        roles_count = Role.query.count()
        user_roles_count = db.session.execute(text("SELECT COUNT(*) FROM user_roles")).scalar()
        return jsonify({
            'users_count': users_count,
            'roles_count': roles_count,
            'user_roles_count': user_roles_count
        })
    except Exception as e:
        current_app.logger.error(f"Error in test_creation: {e}")
        return jsonify({'error': str(e)}), 500

@swagger_bp.route('/test-sites', methods=['GET'])
@swag_from({
    'tags': ['Database Tests'],
    'description': 'Récupère et retourne la liste de tous les sites dans la base de données.',
    'responses': {
        200: {
            'description': 'Liste des sites.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'example': 1},
                        'name': {'type': 'string', 'example': 'Site 1'},
                    }
                }
            }
        },
        500: {'description': 'Erreur lors de la récupération des sites.'}
    }
})
def test_sites():
    try:
        sites = Site.query.all()
        sites_data = [{'id': site.id, 'name': site.name} for site in sites]
        return jsonify(sites_data)
    except Exception as e:
        current_app.logger.error(f"Error in test_sites: {e}")
        return jsonify({'error': str(e)}), 500

@swagger_bp.route('/test-batiments', methods=['GET'])
@swag_from({
    'tags': ['Database Tests'],
    'description': 'Récupère et retourne la liste de tous les bâtiments dans la base de données.',
    'responses': {
        200: {
            'description': 'Liste des bâtiments.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'example': 1},
                        'name': {'type': 'string', 'example': 'Batiment 1'},
                        'polygon_points': {'type': 'object'}
                    }
                }
            }
        },
        500: {'description': 'Erreur lors de la récupération des bâtiments.'}
    }
})
def test_batiments():
    try:
        batiments = Batiment.query.all()
        batiments_data = [{'id': b.id, 'name': b.name, 'polygon_points': b.polygon_points} for b in batiments]
        return jsonify(batiments_data)
    except Exception as e:
        current_app.logger.error(f"Error in test_batiments: {e}")
        return jsonify({'error': str(e)}), 500

@swagger_bp.route('/test-etages', methods=['GET'])
@swag_from({
    'tags': ['Database Tests'],
    'description': 'Récupère et retourne la liste de tous les étages dans la base de données.',
    'responses': {
        200: {
            'description': 'Liste des étages.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'example': 1},
                        'name': {'type': 'string', 'example': 'Etage 1'}
                    }
                }
            }
        },
        500: {'description': 'Erreur lors de la récupération des étages.'}
    }
})
def test_etages():
    try:
        etages = Etage.query.all()
        etages_data = [{'id': e.id, 'name': e.name} for e in etages]
        return jsonify(etages_data)
    except Exception as e:
        current_app.logger.error(f"Error in test_etages: {e}")
        return jsonify({'error': str(e)}), 500

@swagger_bp.route('/test-baes', methods=['GET'])
@swag_from({
    'tags': ['Database Tests'],
    'description': 'Récupère et retourne la liste de tous les BAES dans la base de données.',
    'responses': {
        200: {
            'description': 'Liste des BAES.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'example': 1},
                        'name': {'type': 'string', 'example': 'BAES 1'},
                        'position': {'type': 'object'}
                    }
                }
            }
        },
        500: {'description': 'Erreur lors de la récupération des BAES.'}
    }
})
def test_baes():
    try:
        baes_list = BAES.query.all()
        baes_data = [{'id': b.id, 'name': b.name, 'position': b.position} for b in baes_list]
        return jsonify(baes_data)
    except Exception as e:
        current_app.logger.error(f"Error in test_baes: {e}")
        return jsonify({'error': str(e)}), 500

@swagger_bp.route('/test-historique', methods=['GET'])
@swag_from({
    'tags': ['Database Tests'],
    'description': "Récupère et retourne la liste de tous les historiques d'erreur dans la base de données.",
    'responses': {
        200: {
            'description': "Liste des historiques d'erreur.",
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'example': 1},
                        'baes_id': {'type': 'integer', 'example': 1},
                        'type_erreur': {'type': 'string', 'example': 'erreur_connexion'},
                        'timestamp': {'type': 'string', 'format': 'date-time'}
                    }
                }
            }
        },
        500: {'description': "Erreur lors de la récupération de l'historique des erreurs."}
    }
})
def test_historique():
    try:
        historique = HistoriqueErreur.query.all()
        historique_data = [{
            'id': h.id,
            'baes_id': h.baes_id,
            'type_erreur': h.type_erreur,
            'timestamp': h.timestamp.isoformat() if h.timestamp else None
        } for h in historique]
        return jsonify(historique_data)
    except Exception as e:
        current_app.logger.error(f"Error in test_historique: {e}")
        return jsonify({'error': str(e)}), 500

@swagger_bp.route('/test-users', methods=['GET'])
@swag_from({
    'tags': ['Database Tests'],
    'description': "Récupère et retourne la liste de tous les utilisateurs dans la base de données.",
    'responses': {
        200: {
            'description': "Liste des utilisateurs.",
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'example': 1},
                        'login': {'type': 'string', 'example': 'user1'}
                    }
                }
            }
        },
        500: {'description': "Erreur lors de la récupération des utilisateurs."}
    }
})
def test_users():
    try:
        users = User.query.all()
        users_data = [{'id': u.id, 'login': u.login} for u in users]
        return jsonify(users_data)
    except Exception as e:
        current_app.logger.error(f"Error in test_users: {e}")
        return jsonify({'error': str(e)}), 500

@swagger_bp.route('/test-roles', methods=['GET'])
@swag_from({
    'tags': ['Database Tests'],
    'description': "Récupère et retourne la liste de tous les rôles dans la base de données.",
    'responses': {
        200: {
            'description': "Liste des rôles.",
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'example': 1},
                        'name': {'type': 'string', 'example': 'admin'}
                    }
                }
            }
        },
        500: {'description': "Erreur lors de la récupération des rôles."}
    }
})
def test_roles():
    try:
        roles = Role.query.all()
        roles_data = [{'id': r.id, 'name': r.name} for r in roles]
        return jsonify(roles_data)
    except Exception as e:
        current_app.logger.error(f"Error in test_roles: {e}")
        return jsonify({'error': str(e)}), 500

#####################################
# Endpoints pour la gestion des cartes
#####################################

@swagger_bp.route('/carte/upload', methods=['POST'])
@swag_from({
    'tags': ['Carte Operations'],
    'description': "Upload d'une carte. Fournissez un fichier via le champ 'file'.",
    'consumes': ["multipart/form-data"],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Fichier image à uploader (png, jpg, jpeg, gif)'
        }
    ],
    'responses': {
        200: {
            'description': "Fichier uploadé avec succès.",
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Fichier uploadé avec succès'},
                    'chemin': {'type': 'string', 'example': 'uploads/monfichier.png'}
                }
            }
        },
        400: {'description': "Erreur d'upload, vérifiez le fichier fourni."}
    }
})
def swagger_upload_carte():
    # Délégation à la logique d'upload définie dans routes/carte_routes.py
    from routes.carte_routes import upload_carte
    return upload_carte()

@swagger_bp.route('/carte/download/<int:carte_id>', methods=['GET'])
@swag_from({
    'tags': ['Carte Operations'],
    'description': "Téléchargement d'une carte via son ID.",
    'parameters': [
        {
            'name': 'carte_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la carte à télécharger'
        }
    ],
    'responses': {
        200: {'description': 'Fichier retourné avec succès.'},
        404: {'description': 'Carte non trouvée.'}
    }
})
def swagger_download_carte(carte_id):
    from routes.carte_routes import download_carte
    return download_carte(carte_id)

@swagger_bp.route('/carte/delete/<int:carte_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Carte Operations'],
    'description': "Supprime une carte via son ID.",
    'parameters': [
        {
            'name': 'carte_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la carte à supprimer'
        }
    ],
    'responses': {
        200: {
            'description': 'Carte supprimée avec succès.',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Carte supprimée avec succès'}
                }
            }
        },
        404: {'description': 'Carte non trouvée.'}
    }
})
def swagger_delete_carte(carte_id):
    from models.carte import Carte
    carte = Carte.query.get(carte_id)
    if not carte:
        return jsonify({'error': 'Carte non trouvée'}), 404
    db.session.delete(carte)
    db.session.commit()
    return jsonify({'message': 'Carte supprimée avec succès'}), 200

@swagger_bp.route('/carte/get/<int:carte_id>', methods=['GET'])
@swag_from({
    'tags': ['Carte Operations'],
    'description': "Récupère les informations d'une carte via son ID.",
    'parameters': [
        {
            'name': 'carte_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la carte à récupérer'
        }
    ],
    'responses': {
        200: {
            'description': "Informations de la carte.",
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'example': 1},
                    'chemin': {'type': 'string', 'example': 'uploads/monfichier.png'}
                }
            }
        },
        404: {'description': 'Carte non trouvée.'}
    }
})
def swagger_get_carte(carte_id):
    from models.carte import Carte
    carte = Carte.query.get(carte_id)
    if not carte:
        return jsonify({'error': 'Carte non trouvée'}), 404
    return jsonify({'id': carte.id, 'chemin': carte.chemin}), 200
