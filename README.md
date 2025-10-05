# 🔥 FireFlow

**FireFlow** est une application Flask qui permet de gérer :
- des **firewalls**
- des **policies (politiques de filtrage)**
- des **règles de firewall (rules)**
- des **utilisateurs** avec authentification JWT

L’application expose des **API REST documentées via Swagger** et stocke les données dans une base **SQLite**.

---

## 🚀 **Prérequis**

- Python **3.13.7** ou supérieur
- (Optionnel) Docker, si vous souhaitez le lancer dans un conteneur

---

## ⚙️ **Installation et lancement WINDOWS**

### ▶️ Lancer avec le script `startapp.bat` (UNIQUEMENT sous Windows)

    Dans un terminal :

    startapp.bat

---

## ⚙️ **Installation et lancement Docker**

    Le fichier dockerfile permet de lancer le projet dans un conteneur

 **Utilisation des endpoints protegés**

    Les routes (/firewalls, /policies, /rules, etc.) sont protégées par JWT.
    Pour les tester depuis Swagger UI, il faut fournir le token d’authentification dans la fenêtre Authorize :

    ''

    Créer un utilisateur (si nécessaire) L'utilisateur "user:123 | password:123 est deja créé "" :


    POST /users/register — envoyer :

    {
      "username": "admin",
      "password": "pass"
    }


    Se connecter pour obtenir le token :
    POST /users/login — envoyer :

    {
      "username": "admin",
      "password": "pass"
    }


    La réponse contiendra :

    {
      "access_token": "<votre_token_JWT>"
    }


    Autoriser Swagger :

    Ouvrir Swagger UI (ex. http://127.0.0.1:5000/swagger/).

    Cliquer sur le bouton Authorize (en haut à droite).

    Dans le champ qui s’affiche, colle exactement :

    Bearer <votre_token_JWT>


    (⚠️ Ne pas oublier le mot Bearer suivi d’un espace avant le token.)

    Clique sur Authorize, puis Close.