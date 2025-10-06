
from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from app.extensions import db
from .models import Firewall, FilteringPolicy, FirewallRule
from .schemas import (
    FirewallSchema, FirewallCreateSchema,
    FilteringPolicySchema, FilteringPolicyCreateSchema,
    FirewallRuleSchema, FirewallRuleCreateSchema
)

ns = Namespace("fireflow", description="Gestion des firewalls, policies et règles")

# --- RESTX models pour Swagger ---
firewall_model = ns.model("Firewall", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True),
    "description": fields.String(),
    "created_at": fields.DateTime(readonly=True)
})
firewall_create_model = ns.model("FirewallCreate", {
    "name": fields.String(required=True),
    "description": fields.String()
})

policy_model = ns.model("FilteringPolicy", {
    "id": fields.Integer(readonly=True),
    "firewall_id": fields.Integer(required=True),
    "name": fields.String(required=True),
    "description": fields.String(),
    "created_at": fields.DateTime(readonly=True)
})
policy_create_model = ns.model("FilteringPolicyCreate", {
    "name": fields.String(required=True),
    "description": fields.String()
})

rule_model = ns.model("FirewallRule", {
    "id": fields.Integer(readonly=True),
    "policy_id": fields.Integer(required=True),
    "action": fields.String(required=True, enum=["ALLOW", "DENY"]),
    "src_ip": fields.String(),
    "dst_ip": fields.String(),
    "src_port": fields.Integer(),
    "dst_port": fields.Integer(),
    "protocol": fields.String(enum=["TCP", "UDP", "ICMP"]),
    "position": fields.Integer(),
    "created_at": fields.DateTime(readonly=True)
})
rule_create_model = ns.model("FirewallRuleCreate", {
    "action": fields.String(required=True, enum=["ALLOW", "DENY"]),
    "src_ip": fields.String(),
    "dst_ip": fields.String(),
    "src_port": fields.Integer(),
    "dst_port": fields.Integer(),
    "protocol": fields.String(enum=["TCP", "UDP", "ICMP"]),
    "position": fields.Integer()
})

# --- SCHEMAS instances ---
firewall_schema = FirewallSchema()
firewalls_schema = FirewallSchema(many=True)
firewall_create_schema = FirewallCreateSchema()

policy_schema = FilteringPolicySchema()
policies_schema = FilteringPolicySchema(many=True)
policy_create_schema = FilteringPolicyCreateSchema()

rule_schema = FirewallRuleSchema()
rules_schema = FirewallRuleSchema(many=True)
rule_create_schema = FirewallRuleCreateSchema()

# -----------------------
# FIREWALLS
# -----------------------
@ns.route("/firewalls")
class FirewallList(Resource):
    @jwt_required()
    def get(self):
        firewalls = Firewall.query.all()
        return firewalls_schema.dump(firewalls), 200

    @jwt_required()
    @ns.expect(firewall_create_model, validate=True)
    def post(self):
        if not request.is_json:
            return {"error": "Request must be JSON"}, 400
        data = request.get_json()
        errors = firewall_create_schema.validate(data)
        if errors:
            return {"errors": errors}, 400
        firewall = Firewall(**data)
        db.session.add(firewall)
        db.session.commit()
        return firewall_schema.dump(firewall), 201

@ns.route("/firewalls/<int:fw_id>")
class FirewallDetail(Resource):
    @jwt_required()
    def get(self, fw_id):
        fw = Firewall.query.get_or_404(fw_id)
        return firewall_schema.dump(fw), 200

    @jwt_required()
    def delete(self, fw_id):
        fw = Firewall.query.get_or_404(fw_id)
        db.session.delete(fw)
        db.session.commit()
        return "", 204

# -----------------------
# POLICIES (per firewall)
# -----------------------
@ns.route("/firewalls/<int:fw_id>/policies")
class PolicyList(Resource):
    @jwt_required()
    def get(self, fw_id):
        fw = Firewall.query.get_or_404(fw_id)
        return policies_schema.dump(fw.policies), 200

    @jwt_required()
    @ns.expect(policy_create_model, validate=True)
    def post(self, fw_id):
        if not request.is_json:
            return {"error": "Request must be JSON"}, 400
        fw = Firewall.query.get_or_404(fw_id)
        data = request.get_json()
        errors = policy_create_schema.validate(data)
        if errors:
            return {"errors": errors}, 400
        # liée au firewall via fw_id
        data["firewall_id"] = fw.id
        policy = FilteringPolicy(**data)
        db.session.add(policy)
        db.session.commit()
        return policy_schema.dump(policy), 201

@ns.route("/policies/<int:policy_id>")
class PolicyDetail(Resource):
    @jwt_required()
    def get(self, policy_id):
        policy = FilteringPolicy.query.get_or_404(policy_id)
        return policy_schema.dump(policy), 200

    @jwt_required()
    def delete(self, policy_id):
        policy = FilteringPolicy.query.get_or_404(policy_id)
        db.session.delete(policy)
        db.session.commit()
        return "", 204

# -----------------------
# RULES (per policy)
# -----------------------
@ns.route("/policies/<int:policy_id>/rules")
class RuleList(Resource):
    @jwt_required()
    def get(self, policy_id):
        policy = FilteringPolicy.query.get_or_404(policy_id)
        return rules_schema.dump(policy.rules), 200

    @jwt_required()
    @ns.expect(rule_create_model, validate=True)
    def post(self, policy_id):
        if not request.is_json:
            return {"error": "Request must be JSON"}, 400
        policy = FilteringPolicy.query.get_or_404(policy_id)
        data = request.get_json()
        errors = rule_create_schema.validate(data)
        if errors:
            return {"errors": errors}, 400
        # lier la règle à la policy
        data["policy_id"] = policy.id
        rule = FirewallRule(**data)
        db.session.add(rule)
        db.session.commit()
        return rule_schema.dump(rule), 201

@ns.route("/rules/<int:rule_id>")
class RuleDetail(Resource):
    @jwt_required()
    def get(self, rule_id):
        rule = FirewallRule.query.get_or_404(rule_id)
        return rule_schema.dump(rule), 200

    @jwt_required()
    def delete(self, rule_id):
        rule = FirewallRule.query.get_or_404(rule_id)
        db.session.delete(rule)
        db.session.commit()
        return "", 204
