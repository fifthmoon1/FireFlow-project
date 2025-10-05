#!/bin/bash
set -e

echo "-------------------------------"
echo "Démarrage du conteneur FireFlow"
echo "-------------------------------"

# Vérifier si la base existe
if [ ! -f /usr/src/app/fireflow.sqlite ]; then
    echo "Base de données inexistante, création et seed..."

    # Initialisation des migrations si besoin
    if [ ! -d /usr/src/app/migrations ]; then
        flask db init
    fi

    # Créer et appliquer les migrations
    flask db migrate -m "init"
    flask db upgrade

    # Seed des firewalls
    python -m fireflow.seed_firewalls || echo "Erreur lors du seed, vérifier la DB"

    # Seed utilisateur
    python -m users.seed_users || echo "Erreur lors du seed utilisateur"
else
    echo "Base de données déjà existante, pas de seed effectué."
fi

echo "-------------------------------"
echo "Lancement de Flask..."
exec flask run --host=0.0.0.0
