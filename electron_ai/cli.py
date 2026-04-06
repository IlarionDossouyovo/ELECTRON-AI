"""
ELECTRON AI CLI - Interface en ligne de commande
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

from agents.analyzer import AnalyzerAgent
from agents.coder import CoderAgent
from agents.deployer import DeployerAgent
from notifications.n8n import N8NNotifier
from storage.firebase import FirebaseStorage


async def run_full_workflow(
    project_path: str,
    repo_name: str,
    skip_notifications: bool = False,
):
    """Exécute le workflow complet ELECTRON AI"""
    
    print("\n🤖 ELECTRON AI - Démarrage du workflow\n")
    print("=" * 50)
    
    # Initialiser les agents
    analyzer = AnalyzerAgent()
    coder = CoderAgent()
    deployer = DeployerAgent()
    notifier = N8NNotifier()
    storage = FirebaseStorage()
    
    # Étape 1: Analyse
    print("\n📊 Étape 1: Analyse du projet...")
    analysis = await analyzer.analyze(project_path)
    print(f"   ✅ Projet: {analysis.get('project_name', 'N/A')}")
    print(f"   📁 Fichiers: {analysis.get('files_count', 0)}")
    print(f"   🛠 Tech: {', '.join(analysis.get('tech_stack', [])) or 'Non détecté'}")
    
    if not skip_notifications and notifier.enabled:
        await notifier.notify_analysis(
            analysis.get("project_name", "Unknown"),
            analysis.get("files_count", 0),
            analysis.get("tech_stack", []),
        )
    
    # Sauvegarder l'analyse
    if storage._initialized:
        await storage.save_project({
            "name": analysis.get("project_name"),
            "analysis": analysis,
        })
    
    # Étape 2: Déploiement
    print("\n🚀 Étape 2: Déploiement...")
    deployment = await deployer.deploy_to_github(project_path, repo_name)
    
    if "error" in deployment:
        print(f"   ❌ Erreur: {deployment['error']}")
    else:
        print(f"   ✅ GitHub: {deployment.get('url', 'N/A')}")
    
    if not skip_notifications and notifier.enabled:
        await notifier.notify_deployment(
            repo_name,
            deployment.get("url", "N/A"),
            "success" if "error" not in deployment else "failed",
        )
    
    print("\n" + "=" * 50)
    print("✅ Workflow terminé !")
    
    return {
        "analysis": analysis,
        "deployment": deployment,
    }


def main():
    """Point d'entrée CLI"""
    parser = argparse.ArgumentParser(
        description="ELECTRON AI - Système multi-agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  electron-ai run --project /chemin/vers/projet --repo mon-projet
  electron-ai analyze --project /chemin/vers/projet
  electron-ai deploy --project /chemin/vers/projet --repo mon-projet
        """,
    )
    
    parser.add_argument("--version", action="version", version="ELECTRON AI 0.1.0")
    
    subparsers = parser.add_subparsers(dest="command", help="Commandes")
    
    # Commande run
    run_parser = subparsers.add_parser("run", help="Exécute le workflow complet")
    run_parser.add_argument("--project", required=True, help="Chemin du projet")
    run_parser.add_argument("--repo", required=True, help="Nom du dépôt GitHub")
    run_parser.add_argument("--skip-notifications", action="store_true", help="Désactiver les notifications")
    
    # Commande analyze
    analyze_parser = subparsers.add_parser("analyze", help="Analyse un projet")
    analyze_parser.add_argument("--project", required=True, help="Chemin du projet")
    
    # Commande deploy
    deploy_parser = subparsers.add_parser("deploy", help="Déploie sur GitHub et Vercel")
    deploy_parser.add_argument("--project", required=True, help="Chemin du projet")
    deploy_parser.add_argument("--repo", required=True, help="Nom du dépôt GitHub")
    
    # Parser les arguments
    args = parser.parse_args()
    
    if args.command == "run":
        asyncio.run(run_full_workflow(
            args.project,
            args.repo,
            args.skip_notifications,
        ))
    elif args.command == "analyze":
        analyzer = AnalyzerAgent()
        result = asyncio.run(analyzer.analyze(args.project))
        print(result)
    elif args.command == "deploy":
        deployer = DeployerAgent()
        result = asyncio.run(deployer.deploy_to_github(args.project, args.repo))
        print(result)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()