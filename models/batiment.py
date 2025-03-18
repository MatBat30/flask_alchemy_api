from sqlalchemy import text

from . import db


class Batiment(db.Model):
    __tablename__ = 'batiments'

    id = db.Column(db.Integer, primary_key=True)
    polygon_points = db.Column(db.JSON)
    name = db.Column(db.String(50), nullable=False)
    # La clé étrangère est optionnelle (nullable=True) car un bâtiment peut ne pas appartenir à un site.
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=True)
    # Relation one-to-many : Un bâtiment a plusieurs étages.
    etages = db.relationship('Etage', backref='batiment', lazy=True)

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
        return f"<Batiment {self.name}>"
