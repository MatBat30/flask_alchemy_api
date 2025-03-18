from sqlalchemy import text

from . import db


class Site(db.Model):
    __tablename__ = 'sites'
    __table_args__ = {'extend_existing': True}  # Permet de redéfinir la table si elle existe déjà

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    batiments = db.relationship('Batiment', backref='site', lazy=True)

    # One-to-one vers Carte via site_id
    carte = db.relationship('Carte', backref='site', uselist=False, foreign_keys='Carte.site_id')

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
        return f"<Site {self.name}>"
