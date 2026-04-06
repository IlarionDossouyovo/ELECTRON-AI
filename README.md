# ELECTRON AI 🤖

Système d'Intelligence Artificielle multi-agents pour automatiser le développement, déploiement et notification de projets web.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ELECTRON AI                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                 │
│  │  ANALYZER   │───▶│   CODER     │───▶│   DEPLOYER   │                 │
│  │    Agent   │    │    Agent    │    │    Agent    │                 │
│  └─────┬──────┘    └──────┬──────┘    └──────┬──────┘                 │
│        │                  │                  │                         │
│        ▼                  ▼                  ▼                         │
│  ┌─────────────────────────────────────────────────────┐               │
│  │                  FIREBASE STORE                    │               │
│  └───────────────────────┬─────────────────────────┘               │
│                          │                                           │
│                          ▼                                           │
│  ┌─────────────────────────────────────────────────────┐               │
│  │              N8N WORKFLOW (WhatsApp)                │               │
│  └─────────────────────────────────────────────────────┘               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Workflow

1. **Input** → OpenHands Cloud reçoit le projet
2. **Analyzer** → Analyse le projet (code, dépendances, structure)
3. **Coder** → Génère/met à jour le code
4. **Deployer** → Pousse sur GitHub + Déploie sur Vercel
5. **Storage** → Stocke données sur Firebase
6. **Notifier** → N8N notifie sur WhatsApp

## Installation

```bash
# Clone le projet
git clone https://github.com/TON_COMPTE/electron-ai.git
cd electron-ai

# Installation Python
uv sync

# Installation Node.js
npm install
```

## Configuration

Crée un fichier `.env` :

```env
# GitHub
GITHUB_TOKEN=ton_token_github

# Vercel
VERCEL_TOKEN=ton_token_vercel
VERCEL_PROJECT_ID=ton_project_id

# Firebase
FIREBASE_API_KEY=ton_api_key
FIREBASE_PROJECT_ID=ton_project_id
FIREBASE_PRIVATE_KEY=ton_private_key
FIREBASE_CLIENT_EMAIL=ton_email

# N8N
N8N_URL=ton_url_n8n
N8N_API_KEY=ton_api_key_n8n

# WhatsApp (Twilio ou autre)
TWILIO_ACCOUNT_SID=ton_sid
TWILIO_AUTH_TOKEN=ton_token
TWILIO_PHONE_NUMBER=ton_numero
```

## Utilisation

### Mode CLI

```bash
python -m electron_ai.cli --help
python -m electron_ai.cli run --project "chemin/vers/projet"
```

### Mode API

```bash
uvicorn electron_ai.api:app --reload
```

### Avec n8n

```bash
# Démarre le webhook watcher
python -m electron_ai.webhook
```

## Structure du Projet

```
electron-ai/
├── electron_ai/
│   ├── __init__.py
│   ├── cli.py          # Interface CLI
│   ├── api.py          # API FastAPI
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── analyzer.py    # Agent Analyzer
│   │   ├── coder.py      # Agent Coder
│   │   └── deployer.py  # Agent Deployer
│   ├── storage/
│   │   └── firebase.py  # Stockage Firebase
│   ├── notifications/
│   │   └── n8n.py      # Notifications N8N
│   └── webhook/
│       └── watcher.py    # Webhook n8n
├── pyproject.toml
├── uv.lock
├── .env.example
└── README.md
```

## License

MIT