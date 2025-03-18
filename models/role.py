from sqlalchemy import text

from . import db


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

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
        return f"<Role {self.name}>"
