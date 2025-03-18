from sqlalchemy import text

from . import db


class BAES(db.Model):
    __tablename__ = 'baes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    position = db.Column(db.JSON, nullable=False)

    # La clé étrangère est optionnelle (nullable=True) car une BAES ne peut pas ne pas être affectée à un étage.
    etage_id = db.Column(db.Integer, db.ForeignKey('etages.id'), nullable=False)
    erreurs = db.relationship('HistoriqueErreur', backref='baes', lazy=True)

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
        return f"<BAES {self.name}>"
