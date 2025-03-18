# app.py
import logging
import os
import urllib

import pyodbc
from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from models import db

# Initialisation de l'application
app = Flask(__name__)
CORS(app)
# Configuration de la connexion à la base (SQL Server par exemple)
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=127.0.0.1;"
    "DATABASE=master;"
    "UID=Externe;"
    "PWD=Secur3P@ssw0rd!"
)
params = urllib.parse.quote_plus(connection_string)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

# Configuration pour l'upload de fichiers
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 16 MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Initialisation de Flask-SQLAlchemy, Flask-Migrate et Swagger
db.init_app(app)
migrate = Migrate(app, db)
swagger = Swagger(app)

# Enregistrement des blueprints depuis le dossier routes
from routes import init_app as init_routes
init_routes(app)

# Fonction pour créer les données par défaut
def create_default_data():
    app.logger.debug("Création des données par défaut...")
    default_roles = ['user', 'technicien', 'admin', 'super-admin']
    roles = {}
    from models.role import Role  # Assurez-vous que le modèle est bien importé ici

    for role_name in default_roles:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.session.add(role)
            app.logger.debug("Création du rôle %s", role_name)
        roles[role_name] = role
    db.session.commit()

    default_users = {
        'user': {'login': 'user', 'password': 'user_password'},
        'technicien': {'login': 'technicien', 'password': 'tech_password'},
        'admin': {'login': 'admin', 'password': 'admin_password'},
        'super-admin': {'login': 'superadmin', 'password': 'superadmin_password'},
    }
    from models.user import User  # Importez le modèle User
    for role_name, user_data in default_users.items():
        user = User.query.filter_by(login=user_data['login']).first()
        if not user:
            user = User(login=user_data['login'], password=user_data['password'])
            user.roles.append(roles[role_name])
            db.session.add(user)
            app.logger.debug("Création de l'utilisateur %s associé au rôle %s", user_data['login'], role_name)
    db.session.commit()

if __name__ == '__main__':
    app.logger.debug("Démarrage de l'application et test de connexion à la base...")
    print("Pilotes ODBC installés :", pyodbc.drivers())
    with app.app_context():
        try:
            connection = db.engine.connect()
            connection.close()
            app.logger.debug("Connexion réussie à la base de données.")
        except Exception as e:
            app.logger.error("Erreur de connexion à la base de données : %s", e)
        create_default_data()
    app.run(debug=True)
