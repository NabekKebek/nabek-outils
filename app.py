from flask import Flask, request, jsonify, send_from_directory
import os
import sqlite3
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='.')

# Configuration
UPLOAD_FOLDER = 'uploads'
DB_PATH = 'coffre.db'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'html', 'md', 'doc', 'docx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def init_db():
    """Crée la base de données si elle n'existe pas."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id TEXT PRIMARY KEY,
            titre TEXT NOT NULL,
            description TEXT,
            keywords TEXT,
            filename TEXT,
            filetype TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()


def generer_id():
    """Génère un ID unique NABEK-AAAA-NNN."""
    now = datetime.now()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM entries')
    count = c.fetchone()[0] + 1
    conn.close()
    return f'NABEK-{now.year}-{str(count).zfill(3)}'


@app.route('/')
def index():
    """Sert la page d'accueil."""
    return send_from_directory('.', 'index.html')


@app.route('/api/ajouter', methods=['POST'])
def ajouter():
    """Ajoute une entrée dans le coffre."""
    titre = request.form.get('titre', '').strip()
    description = request.form.get('description', '').strip()
    keywords = request.form.get('keywords', '').strip()
    fichier = request.files.get('fichier')

    if not titre:
        return jsonify({'error': 'Titre requis'}), 400

    entry_id = generer_id()
    filename = None
    filetype = None

    if fichier and fichier.filename:
        filename = secure_filename(fichier.filename)
        filetype = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'unknown'
        filepath = os.path.join(UPLOAD_FOLDER, f"{entry_id}_{filename}")
        fichier.save(filepath)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO entries (id, titre, description, keywords, filename, filetype, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (entry_id, titre, description, keywords, filename, filetype,
          datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'id': entry_id})


@app.route('/api/voir', methods=['GET'])
def voir():
    """Retourne toutes les entrées du coffre."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM entries ORDER BY date DESC')
    rows = c.fetchall()
    conn.close()

    entries = []
    for row in rows:
        entries.append({
            'id': row[0],
            'titre': row[1],
            'description': row[2],
            'keywords': [k.strip() for k in row[3].split(',') if k.strip()] if row[3] else [],
            'filename': row[4],
            'filetype': row[5],
            'date': row[6]
        })
    return jsonify(entries)


@app.route('/api/rechercher', methods=['GET'])
def rechercher():
    """Recherche dans le coffre."""
    query = request.args.get('q', '').lower().strip()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if query:
        c.execute('''
            SELECT * FROM entries
            WHERE LOWER(titre) LIKE ?
               OR LOWER(description) LIKE ?
               OR LOWER(keywords) LIKE ?
            ORDER BY date DESC
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
    else:
        c.execute('SELECT * FROM entries ORDER BY date DESC')

    rows = c.fetchall()
    conn.close()

    entries = []
    for row in rows:
        entries.append({
            'id': row[0],
            'titre': row[1],
            'description': row[2],
            'keywords': [k.strip() for k in row[3].split(',') if k.strip()] if row[3] else [],
            'filename': row[4],
            'filetype': row[5],
            'date': row[6]
        })
    return jsonify(entries)


@app.route('/api/requete', methods=['GET'])
def requete():
    """Génère une requête web à partir de tous les mots-clés."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT keywords FROM entries
                 WHERE keywords IS NOT NULL AND keywords != ""''')
    rows = c.fetchall()
    conn.close()

    all_keywords = []
    for row in rows:
        all_keywords.extend([k.strip() for k in row[0].split(',') if k.strip()])

    unique = list(dict.fromkeys(all_keywords))
    return jsonify({'query': ' '.join(unique)})


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
