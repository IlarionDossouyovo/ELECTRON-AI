"""
ELECTRON AI - Système d'Intelligence Artificielle multi-agents
pour ELECTRON - Web Design & Marketing Digital au Bénin
"""

import os
from pathlib import Path


def main():
    """Point d'entrée principal de ELECTRON AI"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                       ║
    ║   🤖 ELECTRON AI - Système Multi-Agents                ║
    ║   Web Design & Marketing Digital au Bénin              ║
    ║                                                       ║
    ║   Input → Analyzer → Coder → Deployer → Storage        ║
    ║                    → Notifier (WhatsApp via N8N)       ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    check_env()
    
    print("\n🚀 ELECTRON AI est prêt !")
    print("\nOptions:")
    print("  python -m electron_ai.cli --help  # CLI")
    print("  python -m electron_ai.api         # API")


def check_env():
    """Vérifie la configuration"""
    required = ["GITHUB_TOKEN"]
    missing = [v for v in required if not os.getenv(v)]
    
    if missing:
        print(f"\n⚠️  Variables manquantes: {', '.join(missing)}")
    else:
        print("\n✅ Configuration OK")


if __name__ == "__main__":
    main()
