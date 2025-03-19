from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Tables d'association pour les relations plusieurs-à-plusieurs
user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

user_sites = db.Table(
    'user_sites',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('site_id', db.Integer, db.ForeignKey('sites.id'), primary_key=True)
)

# Importation des modèles une fois que db et les tables d'association sont définis
from .batiment import Batiment
from .role import Role
from .site import Site
from .carte import Carte
from .etage import Etage
from .baes import Baes
from .historique_erreur import HistoriqueErreur
from .user import User
