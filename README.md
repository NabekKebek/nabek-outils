[README.md](https://github.com/user-attachments/files/31553754/README.md)
# Coffre Numérique Nabek — Outil en ligne

## Greffon outil site web Projet Nabek — V4

Ce dossier contient le **Coffre Numérique Nabek** : un outil de recherche et de classement en ligne.

---

## 📁 Contenu du dossier

| Fichier | Description |
|:---|:---|
| `index.html` | La page web (vitrine + outil Recherche) |
| `app.py` | Le cerveau Python (backend Flask) |
| `requirements.txt` | Les bibliothèques Python nécessaires |
| `robots.txt` | Autorise les robots d'indexation |
| `sitemap.xml` | Plan du site |

---

## 🚀 Comment installer sur PythonAnywhere (gratuit)

### Étape 1 : Créer un compte
1. Va sur https://www.pythonanywhere.com
2. Crée un compte gratuit
3. Confirme ton email

### Étape 2 : Ouvrir une console Bash
1. Dans le tableau de bord, clique sur **Consoles**
2. Clique sur **Bash**

### Étape 3 : Télécharger les fichiers
Dans la console Bash, tape ces commandes une par une :

```bash
# Créer le dossier du projet
mkdir nabek-coffre
cd nabek-coffre

# Télécharger les fichiers (tu devras les uploader manuellement via Files)
# OU utiliser git si tu as mis le projet sur GitHub
```

**Méthode simple** : Va dans l'onglet **Files**, navigue vers `nabek-coffre/`, et upload chaque fichier.

### Étape 4 : Installer les dépendances
```bash
pip3 install -r requirements.txt --user
```

### Étape 5 : Créer l'application web
1. Va dans l'onglet **Web**
2. Clique sur **Add a new web app**
3. Choisis **Manual configuration**
4. Choisis **Python 3.10**
5. Dans **WSGI configuration file**, clique sur le lien et remplace le contenu par :

```python
import sys
path = '/home/TON_NOM_UTILISATEUR/nabek-coffre'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

(Remplace `TON_NOM_UTILISATEUR` par ton vrai nom d'utilisateur PythonAnywhere.)

### Étape 6 : Redémarrer l'application
1. Retourne dans l'onglet **Web**
2. Clique sur **Reload**
3. Ton site est en ligne !

---

## 🔒 Rendre le site privé

Dans `app.py`, ajoute une protection par mot de passe avant la ligne `app = Flask(__name__)` :

```python
from functools import wraps
from flask import request, Response

def check_auth(username, password):
    return username == 'nabek' and password == 'TON_MOT_DE_PASSE'

def authenticate():
    return Response('Accès refusé.', 401,
        {'WWW-Authenticate': 'Basic realm="Coffre Nabek"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
```

Puis ajoute `@requires_auth` avant chaque route API.

---

## 📝 Fonctionnement

| Bouton | Action |
|:---|:---|
| **Rechercher** | Cherche dans toutes les entrées du coffre |
| **Ajouter** | Ouvre un formulaire pour ranger une entrée + fichier |
| **Voir le coffre** | Affiche toutes les entrées |
| **Requête web** | Rassemble tous les mots-clés et ouvre Google |

---

## 🗄️ Base de données

Les entrées sont stockées dans une base SQLite (`coffre.db`) et les fichiers dans le dossier `uploads/`.

---

*Coffre Numérique Nabek — Greffon outil site web Projet Nabek*
