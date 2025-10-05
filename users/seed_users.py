from app import create_app, db
from users.models import User  # Assure-toi que le package users a bien un fichier models.py
from dotenv import load_dotenv

load_dotenv()  # Charge les variables d'environnement si nécessaire

app = create_app()

DEFAULT_USERNAME = "123"
DEFAULT_PASSWORD = "123"

with app.app_context():
    # Vérifie si l'utilisateur existe déjà
    if User.query.filter_by(username=DEFAULT_USERNAME).first():
        print(f"L'utilisateur {DEFAULT_USERNAME} existe déjà, seed ignoré.")
    else:
        user = User(username=DEFAULT_USERNAME)
        user.set_password(DEFAULT_PASSWORD)
        db.session.add(user)
        db.session.commit()
        print(f"Utilisateur '{DEFAULT_USERNAME}' créé avec succès ! Mot de passe : '{DEFAULT_PASSWORD}'")
