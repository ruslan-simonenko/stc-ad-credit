from persistence import db


class CarbonAuditorEntity(db.Model):
    __tablename__ = 'carbon_auditor'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    name = db.Column(db.String)
    picture_url = db.Column(db.String)
