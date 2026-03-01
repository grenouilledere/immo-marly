import os
import json
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='static')

# ── Servir le frontend ──────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

# ── Proxy sécurisé vers l'API Anthropic ────────────────────────
@app.route('/api/chat', methods=['POST'])
def chat():
    # Lire la clé à chaque requête (pas au démarrage)
    api_key = os.environ.get('ANTHROPIC_API_KEY', '').strip()
    if not api_key:
        return jsonify({'error': 'Clé API ANTHROPIC_API_KEY non configurée sur le serveur'}), 500

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Requete invalide'}), 400

    system_prompt = data.get('system', '')
    messages = data.get('messages', [])

    try:
        resp = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json',
            },
            json={
                'model': 'claude-haiku-4-5-20251001',
                'max_tokens': 1024,
                'system': system_prompt,
                'messages': messages,
            },
            timeout=30
        )
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Delai depasse, reessayez'}), 504
    except requests.exceptions.HTTPError as e:
        return jsonify({'error': f'Erreur API {resp.status_code} — verifiez la cle API dans Render'}), resp.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 502

# ── Route de diagnostic ─────────────────────────────────────────
@app.route('/api/status')
def status():
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    return jsonify({
        'status': 'ok',
        'api_key_configured': bool(api_key),
        'api_key_prefix': api_key[:10] + '...' if api_key else 'NON DEFINIE'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
