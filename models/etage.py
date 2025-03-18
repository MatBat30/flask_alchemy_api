from sqlalchemy import text

from . import db


class Etage(db.Model):
    __tablename__ = 'etages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    batiment_id = db.Column(db.Integer, db.ForeignKey('batiments.id'), nullable=False)

    # One-to-one vers Carte via etage_id
    carte = db.relationship('Carte', backref='etage', uselist=False, foreign_keys='Carte.etage_id')

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
        return f"<Etage {self.name}>"
