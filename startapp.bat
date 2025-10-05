@echo off
REM -------------------------------
REM Démarrage de l'application UNIQUEMENT POUR WINDOWS
REM -------------------------------

REM Création de l'environnement virtuel si inexistant
if not exist venv (
    echo Création de l'environnement virtuel...
    python -m venv venv
)

REM Activation de l'environnement virtuel
echo --------------------------------------------
echo Activation de l'environnement virtuel...
call venv\Scripts\activate

REM Installation des dépendances
if exist requirements.txt (
    echo --------------------------------------------
    echo Installation des dépendances...
    pip install --upgrade pip
    pip install -r requirements.txt
)

REM Définir l'application Flask
set FLASK_APP=app.manage
set FLASK_ENV=development
set FLASK_DEBUG=1

REM Initialisation des migrations si besoin
if not exist migrations (
    echo --------------------------------------------
    echo Création de la migration initiale...
    flask db init
)

REM Appliquer les migrations
echo --------------------------------------------
echo Création et application des migrations...
flask db migrate -m "init"
flask db upgrade

REM Remplissage de la base uniquement si elle n'existe pas

echo --------------------------------------------
echo Remplissage de la base de données avec les firewalls...
python -m fireflow.seed_firewalls || echo "Erreur lors du seed, vérifier la DB"
REM Seed utilisateur par défaut
echo --------------------------------------------
echo Création de l'utilisateur par défaut...
python -m users.seed_users || echo "Erreur lors du seed des utilisateurs"    



REM Démarrage de l'application Flask
echo --------------------------------------------
echo Démarrage de l'application Flask...
flask run
