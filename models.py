from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Rep(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Prospect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Text)
    color = db.Column(db.String(20))
    demo_date = db.Column(db.Date)
    review_date = db.Column(db.Date)
    onboarding_date = db.Column(db.Date)
    sold = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float)
    product = db.Column(db.String(100))
    integration_fee = db.Column(db.Float)
    package_type = db.Column(db.String(50))

    closer_id = db.Column(db.Integer, db.ForeignKey('rep.id'))
    setter_id = db.Column(db.Integer, db.ForeignKey('rep.id'))

    closer = db.relationship('Rep', foreign_keys=[closer_id])
    setter = db.relationship('Rep', foreign_keys=[setter_id])

class Commission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prospect_id = db.Column(db.Integer, db.ForeignKey('prospect.id'))
    closer_id = db.Column(db.Integer, db.ForeignKey('rep.id'))
    setter_id = db.Column(db.Integer, db.ForeignKey('rep.id'))
    amount = db.Column(db.Float)
    percent = db.Column(db.Float)
    is_recurring = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    prospect = db.relationship('Prospect')
    closer = db.relationship('Rep', foreign_keys=[closer_id])
    setter = db.relationship('Rep', foreign_keys=[setter_id])

