from sqlalchemy import text

from . import db

class Carte(db.Model):
    __tablename__ = 'cartes'
    id = db.Column(db.Integer, primary_key=True)
    chemin = db.Column(db.String(255), nullable=False)
    # La carte peut être liée à un seul étage ou à un seul site (mais pas les deux)
    etage_id = db.Column(db.Integer, db.ForeignKey('etages.id'), nullable=True, unique=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=True, unique=True)

    __table_args__ = (
        db.CheckConstraint(
            '((etage_id IS NOT NULL AND site_id IS NULL) OR (etage_id IS NULL AND site_id IS NOT NULL))',
            name='ck_carte_one_relation'
        ),
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
        return f"<Carte {self.chemin}>"
