from app.extensions import db
from sqlalchemy import func

class Firewall(db.Model):
    __tablename__ = "firewalls"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.String(512))
    created_at = db.Column(db.DateTime, server_default=func.now())

    policies = db.relationship("FilteringPolicy", backref="firewall", cascade="all, delete-orphan")

class FilteringPolicy(db.Model):
    __tablename__ = "policies"
    id = db.Column(db.Integer, primary_key=True)
    firewall_id = db.Column(db.Integer, db.ForeignKey("firewalls.id"), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512))
    created_at = db.Column(db.DateTime, server_default=func.now())

    rules = db.relationship("FirewallRule", backref="policy", cascade="all, delete-orphan")

class FirewallRule(db.Model):
    __tablename__ = "rules"
    id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey("policies.id"), nullable=False)
    action = db.Column(db.String(10), nullable=False)  # ALLOW / DENY
    src_ip = db.Column(db.String(45))
    dst_ip = db.Column(db.String(45))
    src_port = db.Column(db.Integer)
    dst_port = db.Column(db.Integer)
    protocol = db.Column(db.String(10))
    position = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, server_default=func.now())
