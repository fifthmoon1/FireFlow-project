# fireflow/seed_firewalls.py
from app import create_app, db
from faker import Faker
import random

app = create_app()
fake = Faker()
ACTIONS = ["ALLOW", "DENY"]
PROTOCOLS = ["TCP", "UDP", "ICMP"]

with app.app_context():
    from fireflow.models import Firewall, FilteringPolicy, FirewallRule

    for i in range(10):
        fw = Firewall(name=f"Firewall-{i+1}", description=fake.sentence())
        db.session.add(fw)
        db.session.flush()

        # 1-3 policies per firewall
        for p in range(random.randint(1, 3)):
            policy = FilteringPolicy(
                firewall_id=fw.id,
                name=f"Policy-{p+1}",
                description=fake.sentence()
            )
            db.session.add(policy)
            db.session.flush()

            # 1-5 rules per policy
            for r in range(random.randint(1, 5)):
                rule = FirewallRule(
                    policy_id=policy.id,
                    action=random.choice(ACTIONS),
                    src_ip=fake.ipv4(),
                    dst_ip=fake.ipv4(),
                    src_port=random.randint(1024, 65535),
                    dst_port=random.randint(1, 1024),
                    protocol=random.choice(PROTOCOLS),
                    position=r
                )
                db.session.add(rule)

    db.session.commit()
    print("Seed done: created firewalls, policies and rules")
