from sqlalchemy import DateTime, text

from . import db
from datetime import *  # Importation de datetime

error_types = ('erreur_connexion', 'erreur_batterie')

class HistoriqueErreur(db.Model):
    __tablename__ = 'historique_erreur'

    id = db.Column(db.Integer, primary_key=True)
    baes_id = db.Column(db.Integer, db.ForeignKey('baes.id'), nullable=False)
    type_erreur = db.Column(db.Enum(*error_types, name='type_erreur'), nullable=False)
    timestamp = db.Column(
        DateTime,
        server_default=text("SWITCHOFFSET(SYSDATETIMEOFFSET(), '+01:00')"),
        nullable=False
    )
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
        return f"<HistoriqueErreur(baes_id={self.baes_id}, type_erreur={self.type_erreur}, timestamp={self.timestamp})>"
