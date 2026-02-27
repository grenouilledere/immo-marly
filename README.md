# 🏠 Agent Immobilier — Marly-le-Roi

Application web de suivi du marché immobilier des maisons à Marly-le-Roi (78160).

---

## 🚀 Déploiement sur Render.com (gratuit)

### Étape 1 — Mettre le projet sur GitHub

1. Créez un compte sur [github.com](https://github.com) si vous n'en avez pas
2. Cliquez sur **"New repository"** → nommez-le `immo-marly` → **Public** → **Create**
3. Sur votre ordinateur, installez [GitHub Desktop](https://desktop.github.com) (plus simple)
4. Clonez votre repo, copiez tous les fichiers de ce dossier dedans, puis **Commit & Push**

### Étape 2 — Déployer sur Render

1. Allez sur [render.com](https://render.com) → créez un compte gratuit (avec votre compte GitHub)
2. Cliquez **"New +"** → **"Web Service"**
3. Connectez votre repo GitHub `immo-marly`
4. Render détecte automatiquement la config grâce au `render.yaml`
5. Dans **"Environment Variables"**, ajoutez :
   - **Key** : `ANTHROPIC_API_KEY`
   - **Value** : votre clé API Anthropic (disponible sur [console.anthropic.com](https://console.anthropic.com))
6. Cliquez **"Create Web Service"**

⏳ Le déploiement prend 2-3 minutes. Vous obtenez une URL du type :
`https://immo-marly.onrender.com`

### Étape 3 — Installer sur votre téléphone

**iPhone (Safari) :**
1. Ouvrez l'URL dans Safari
2. Touchez l'icône Partager ↗
3. → "Sur l'écran d'accueil"

**Android (Chrome) :**
1. Ouvrez l'URL dans Chrome
2. Menu ⋮ → "Ajouter à l'écran d'accueil"

---

## 📁 Structure du projet

```
immo-marly/
├── app.py              # Serveur Flask (backend)
├── requirements.txt    # Dépendances Python
├── Procfile           # Commande de démarrage
├── render.yaml        # Config déploiement Render
├── README.md          # Ce fichier
└── static/
    └── index.html     # Application frontend complète
```

---

## 🔑 Clé API Anthropic

La clé API est **uniquement stockée côté serveur** (variable d'environnement Render).
Elle n'est jamais exposée dans le code frontend — c'est le rôle du proxy `/api/chat`.

Pour obtenir une clé : [console.anthropic.com](https://console.anthropic.com)
Coût estimé : quelques centimes par mois pour un usage personnel.

---

## 🛠️ Lancer en local (optionnel)

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=votre_cle_ici
python app.py
# → http://localhost:5000
```

---

## 📊 Données

- **DVF** : 543 transactions réelles (2014–2025) — DGFiP via data.gouv.fr
- **Taux** : 144 points mensuels (2014–2025) — Observatoire Crédit Logement/CSA
