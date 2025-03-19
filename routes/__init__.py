from flask import Blueprint

from .batiment_routes import batiment_bp
from .etage_carte_routes import etage_carte_bp
from .etage_routes import etage_bp
from .site_carte_routes import site_carte_bp
from .site_routes import site_bp
from .carte_routes import carte_bp
from .user_role_routes import user_role_bp
from .user_routes import user_bp
from .user_site_routes import user_site_bp
from .baes_routes import baes_bp
from .historique_erreur_routes import historique_erreur_bp



def init_app(app):
    app.register_blueprint(carte_bp, url_prefix='/cartes')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(user_site_bp, url_prefix='/users/sites')  # Préfixe modifié pour éviter conflit
    app.register_blueprint(site_bp, url_prefix='/sites')
    app.register_blueprint(batiment_bp, url_prefix='/batiments')
    app.register_blueprint(etage_bp, url_prefix='/etages')
    app.register_blueprint(etage_carte_bp, url_prefix='/etages/carte')  # Préfixe modifié pour éviter conflit
    app.register_blueprint(site_carte_bp, url_prefix='/sites/carte')  # Pour la relation one-to-one site-carte
    app.register_blueprint(user_role_bp, url_prefix='/role/users') # Préfixe modifié pour éviter conflit
    app.register_blueprint(baes_bp, url_prefix='/baes')
    app.register_blueprint(historique_erreur_bp, url_prefix='/erreurs')