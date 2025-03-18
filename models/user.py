from sqlalchemy import text

from . import db, user_sites, \
    user_roles  # Assurez-vous d'importer aussi la table user_roles si elle est définie dans __init__.py


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # Relation plusieurs-à-plusieurs avec Role
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))

    # Relation plusieurs-à-plusieurs avec Site
    sites = db.relationship('Site', secondary=user_sites, backref=db.backref('users', lazy='dynamic'))

    created_at = db.Column(
        db.DateTime,
        server_default=text("SWITCHOFFSET(SYSDATETIMEOFFSET(), '+01:00')")
    )
    updated_at = db.Column(
        db.DateTime,
        server_default=text("SWITCHOFFSET(SYSDATETIMEOFFSET(), '+01:00')"),
        server_onupdate=text("SWITCHOFFSET(SYSDATETIMEOFFSET(), '+01:00')")
    )

    def __repr__(self):
        return f"<User {self.login}>"
