from flask.cli import FlaskGroup
from app import create_app
import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
instance_path = os.path.join(basedir, "instance")
os.makedirs(instance_path, exist_ok=True)



app = create_app()
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()
