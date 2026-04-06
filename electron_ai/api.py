"""
ELECTRON AI API - API REST avec FastAPI
"""

import asyncio
import os
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Charger les variables d'environnement
load_dotenv()

from agents.analyzer import AnalyzerAgent
from agents.coder import CoderAgent
from agents.deployer import DeployerAgent
from notifications.n8n import N8NNotifier
from storage.firebase import FirebaseStorage

app = FastAPI(
    title="ELECTRON AI",
    description="Système d'Intelligence Artificielle multi-agents",
    version="0.1.0",
)

# Modèles de données


class AnalyzeRequest(BaseModel):
    project_path: str


class GenerateCodeRequest(BaseModel):
    project_path: str
    prompt: str
    files: dict[str, str] | None = None


class DeployRequest(BaseModel):
    project_path: str
    repo_name: str


class NotificationRequest(BaseModel):
    message: str
    channel: str = "whatsapp"


# Routes


@app.get("/")
async def root():
    """Point d'entrée"""
    return {
        "name": "ELECTRON AI",
        "version": "0.1.0",
        "status": "online",
        "workflow": "Input → Analyzer → Coder → Deployer → Storage → Notifier",
    }


@app.get("/health")
async def health():
    """Santé de l'API"""
    return {"status": "healthy"}


@app.post("/analyze")
async def analyze(request: AnalyzeRequest) -> dict[str, Any]:
    """Analyse un projet"""
    analyzer = AnalyzerAgent()
    return await analyzer.analyze(request.project_path)


@app.post("/generate")
async def generate_code(request: GenerateCodeRequest) -> dict[str, Any]:
    """Génère du code"""
    coder = CoderAgent()
    return await coder.generate(
        request.project_path,
        request.prompt,
        request.files,
    )


@app.post("/deploy")
async def deploy(request: DeployRequest) -> dict[str, Any]:
    """Déploie un projet"""
    deployer = DeployerAgent()
    return await deployer.deploy_to_github(
        request.project_path,
        request.repo_name,
    )


@app.post("/notify")
async def notify(request: NotificationRequest) -> dict[str, Any]:
    """Envoie une notification"""
    notifier = N8NNotifier()
    return await notifier.notify(request.message, request.channel)


@app.post("/workflow")
async def run_workflow(request: DeployRequest) -> dict[str, Any]:
    """Exécute le workflow complet"""
    analyzer = AnalyzerAgent()
    deployer = DeployerAgent()
    notifier = N8NNotifier()
    storage = FirebaseStorage()
    
    # Analyse
    analysis = await analyzer.analyze(request.project_path)
    
    # Déploiement
    deployment = await deployer.deploy_to_github(
        request.project_path,
        request.repo_name,
    )
    
    # Notification
    if "url" in deployment:
        await notifier.notify_deployment(
            request.repo_name,
            deployment["url"],
            "success",
        )
    
    return {
        "analysis": analysis,
        "deployment": deployment,
    }


# Pour tester en local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)