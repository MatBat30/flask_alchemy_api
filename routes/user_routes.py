# routes/user_routes.py
from flask import Blueprint, request, jsonify, current_app
from flasgger import swag_from
from models.user import User
from models import db
from models.role import Role

user_bp = Blueprint('user_bp', __name__)

# routes/user_routes.py
@user_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['User CRUD'],
    'description': 'Récupère la liste de tous les utilisateurs avec leurs sites associés.',
    'responses': {
        200: {
            'description': 'Liste des utilisateurs avec leurs sites.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'example': 1},
                        'login': {'type': 'string', 'example': 'user1'},
                        'roles': {
                            'type': 'array',
                            'items': {'type': 'string'},
                            'example': ['user']
                        },
                        'sites': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'id': {'type': 'integer', 'example': 3},
                                    'name': {'type': 'string', 'example': 'Site test 1'}
                                }
                            },
                            'example': [
                                {'id': 3, 'name': 'Site test 1'},
                                {'id': 4, 'name': 'Site test 2'}
                            ]
                        }
                    }
                }
            }
        },
        500: {'description': 'Erreur interne.'}
    }
})
def get_users():
    try:
        users = User.query.all()
        result = []
        for user in users:
            roles = [role.name for role in user.roles]
            # Pour chaque site, on retourne uniquement l'id et le nom
            sites = [{'id': site.id, 'name': site.name} for site in user.sites]
            result.append({
                'id': user.id,
                'login': user.login,
                'roles': roles,
                'sites': sites
            })
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.error(f"Error in get_users: {e}")
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
@swag_from({
    'tags': ['User CRUD'],
    'description': "Récupère un utilisateur par son ID.",
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': "ID de l'utilisateur à récupérer"
        }
    ],
    'responses': {
        200: {
            'description': "Détails de l'utilisateur.",
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'example': 1},
                    'login': {'type': 'string', 'example': 'user1'},
                    'roles': {'type': 'array', 'items': {'type': 'string'}}
                }
            }
        },
        404: {'description': "Utilisateur non trouvé."},
        500: {'description': "Erreur interne."}
    }
})
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        roles = [role.name for role in user.roles]
        result = {'id': user.id, 'login': user.login, 'roles': roles}
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.error(f"Error in get_user: {e}")
        return jsonify({'error': str(e)}), 500

@user_bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['User CRUD'],
    'description': "Crée un nouvel utilisateur.",
    'consumes': ["application/json"],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'login': {'type': 'string', 'example': 'newuser'},
                    'password': {'type': 'string', 'example': 'newpassword'},
                    'roles': {
                        'type': 'array',
                        'items': {'type': 'string', 'example': 'user'},
                        'description': 'Liste des noms de rôles à associer (optionnel)'
                    }
                },
                'required': ['login', 'password']
            }
        }
    ],
    'responses': {
        201: {
            'description': "Utilisateur créé avec succès.",
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'example': 1},
                    'login': {'type': 'string', 'example': 'newuser'},
                    'roles': {'type': 'array', 'items': {'type': 'string'}}
                }
            }
        },
        400: {'description': "Mauvaise requête."},
        500: {'description': "Erreur interne."}
    }
})
def create_user():
    try:
        data = request.get_json()
        if not data or 'login' not in data or 'password' not in data:
            return jsonify({'error': 'Les champs login et password sont requis'}), 400
        login = data['login']
        password = data['password']
        user = User(login=login, password=password)
        # Association de rôles si fournis
        if 'roles' in data:
            role_names = data['roles']
            roles = Role.query.filter(Role.name.in_(role_names)).all()
            user.roles.extend(roles)
        db.session.add(user)
        db.session.commit()
        result = {'id': user.id, 'login': user.login, 'roles': [role.name for role in user.roles]}
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in create_user: {e}")
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['PUT'])
@swag_from({
    'tags': ['User CRUD'],
    'description': "Met à jour un utilisateur existant par son ID.",
    'consumes': ["application/json"],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': "ID de l'utilisateur à mettre à jour"
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'login': {'type': 'string', 'example': 'updateduser'},
                    'password': {'type': 'string', 'example': 'updatedpassword'},
                    'roles': {
                        'type': 'array',
                        'items': {'type': 'string', 'example': 'admin'},
                        'description': 'Liste des noms de rôles à associer (optionnel)'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': "Utilisateur mis à jour avec succès.",
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'example': 1},
                    'login': {'type': 'string', 'example': 'updateduser'},
                    'roles': {'type': 'array', 'items': {'type': 'string'}}
                }
            }
        },
        404: {'description': "Utilisateur non trouvé."},
        500: {'description': "Erreur interne."}
    }
})
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        data = request.get_json()
        if 'login' in data:
            user.login = data['login']
        if 'password' in data:
            user.password = data['password']
        if 'roles' in data:
            role_names = data['roles']
            roles = Role.query.filter(Role.name.in_(role_names)).all()
            user.roles = roles  # Remplacement de la liste de rôles existante
        db.session.commit()
        result = {'id': user.id, 'login': user.login, 'roles': [role.name for role in user.roles]}
        return jsonify(result), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in update_user: {e}")
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@swag_from({
    'tags': ['User CRUD'],
    'description': "Supprime un utilisateur par son ID.",
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': "ID de l'utilisateur à supprimer"
        }
    ],
    'responses': {
        200: {
            'description': "Utilisateur supprimé avec succès.",
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Utilisateur supprimé avec succès'}
                }
            }
        },
        404: {'description': "Utilisateur non trouvé."},
        500: {'description': "Erreur interne."}
    }
})
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Utilisateur supprimé avec succès'}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error in delete_user: {e}")
        return jsonify({'error': str(e)}), 500
