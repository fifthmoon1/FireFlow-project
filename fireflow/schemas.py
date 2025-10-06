from marshmallow import Schema, fields, validate

# --- FIREWALL ---
class FirewallSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    created_at = fields.DateTime()
    policies = fields.List(fields.Nested(lambda: FilteringPolicySchema()))

class FirewallCreateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()

# --- POLICY ---
class FilteringPolicySchema(Schema):
    id = fields.Int(dump_only=True)
    firewall_id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str()
    created_at = fields.DateTime()
    rules = fields.List(fields.Nested(lambda: FirewallRuleSchema()))

class FilteringPolicyCreateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()

# --- RULE ---
class FirewallRuleSchema(Schema):
    id = fields.Int(dump_only=True)
    policy_id = fields.Int(required=True)
    action = fields.Str(required=True)
    src_ip = fields.Str()
    dst_ip = fields.Str()
    src_port = fields.Int()
    dst_port = fields.Int()
    protocol = fields.Str()
    position = fields.Int()
    created_at = fields.DateTime()

class FirewallRuleCreateSchema(Schema):
    action = fields.Str(required=True, validate=validate.OneOf(["ALLOW", "DENY"]))
    src_ip = fields.Str(required=False)
    dst_ip = fields.Str(required=False)
    src_port = fields.Int()
    dst_port = fields.Int()
    protocol = fields.Str(validate=validate.OneOf(["TCP", "UDP", "ICMP"]))
    position = fields.Int()
