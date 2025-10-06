from app import  db
from fireflow.models import Firewall, FilteringPolicy, FirewallRule

# --- FIREWALLS ---
def test_post_firewall(client, auth_header):
    resp = client.post("/fireflow/firewalls", json={"name": "FW1"}, headers=auth_header)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "FW1"

def test_get_firewalls(client, auth_header):
    fw = Firewall(name="FW-GET")
    db.session.add(fw)
    db.session.commit()
    resp = client.get("/fireflow/firewalls", headers=auth_header)
    assert resp.status_code == 200
    assert any(f["name"] == "FW-GET" for f in resp.get_json())

def test_delete_firewall(client, auth_header):
    fw = Firewall(name="FW-DEL")
    db.session.add(fw)
    db.session.commit()
    resp = client.delete(f"/fireflow/firewalls/{fw.id}", headers=auth_header)
    assert resp.status_code == 204
    assert db.session.get(Firewall, fw.id) is None

# --- POLICIES ---
def test_post_policy(client, auth_header):
    fw = Firewall(name="FW-POL")
    db.session.add(fw)
    db.session.commit()
    resp = client.post(f"/fireflow/firewalls/{fw.id}/policies", json={"name": "P1"}, headers=auth_header)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "P1"
    assert data["firewall_id"] == fw.id

def test_get_policies(client, auth_header):
    fw = Firewall(name="FW-POL-LIST")
    db.session.add(fw)
    db.session.commit()
    pol = FilteringPolicy(name="PolList", firewall_id=fw.id)
    db.session.add(pol)
    db.session.commit()
    resp = client.get(f"/fireflow/firewalls/{fw.id}/policies", headers=auth_header)
    assert resp.status_code == 200
    assert any(p["name"] == "PolList" for p in resp.get_json())

def test_delete_policy(client, auth_header):
    fw = Firewall(name="FW-POL-DEL")
    db.session.add(fw)
    db.session.commit()
    pol = FilteringPolicy(name="PolDel", firewall_id=fw.id)
    db.session.add(pol)
    db.session.commit()
    resp = client.delete(f"/fireflow/policies/{pol.id}", headers=auth_header)
    assert resp.status_code == 204
    assert db.session.get(FilteringPolicy, pol.id) is None

# --- RULES ---
def test_post_rule(client, auth_header):
    fw = Firewall(name="FW-RULE")
    db.session.add(fw)
    db.session.commit()
    pol = FilteringPolicy(name="PolRule", firewall_id=fw.id)
    db.session.add(pol)
    db.session.commit()
    payload = {"action": "ALLOW", "src_ip": "1.1.1.1"}
    resp = client.post(f"/fireflow/policies/{pol.id}/rules", json=payload, headers=auth_header)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["action"] == "ALLOW"
    assert data["policy_id"] == pol.id

def test_get_rules(client, auth_header):
    fw = Firewall(name="FW-RULES-LIST")
    db.session.add(fw)
    db.session.commit()
    pol = FilteringPolicy(name="PolForList", firewall_id=fw.id)
    db.session.add(pol)
    db.session.commit()
    rule = FirewallRule(action="DENY", policy_id=pol.id)
    db.session.add(rule)
    db.session.commit()
    resp = client.get(f"/fireflow/policies/{pol.id}/rules", headers=auth_header)
    assert resp.status_code == 200
    assert any(r["action"] == "DENY" for r in resp.get_json())

def test_delete_rule(client, auth_header):
    fw = Firewall(name="FW-RULE-DEL")
    db.session.add(fw)
    db.session.commit()
    pol = FilteringPolicy(name="PolDelRule", firewall_id=fw.id)
    db.session.add(pol)
    db.session.commit()
    rule = FirewallRule(action="ALLOW", policy_id=pol.id)
    db.session.add(rule)
    db.session.commit()
    resp = client.delete(f"/fireflow/rules/{rule.id}", headers=auth_header)
    assert resp.status_code == 204
    assert db.session.get(FirewallRule, rule.id) is None

