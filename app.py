import os
import json
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='static')

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

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
    if not ANTHROPIC_API_KEY:
        return jsonify({'error': 'Clé API non configurée'}), 500

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Requête invalide'}), 400

    system_prompt = data.get('system', '')
    messages = data.get('messages', [])

    try:
        resp = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'x-api-key': ANTHROPIC_API_KEY,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json',
            },
            json={
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 1000,
                'system': system_prompt,
                'messages': messages,
            },
            timeout=30
        )
        resp.raise_for_status()
        return jsonify(resp.json())

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Délai d\'attente dépassé'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 502


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
