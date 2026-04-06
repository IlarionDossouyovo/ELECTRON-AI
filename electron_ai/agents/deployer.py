"""
Deployer Agent - Déploie les projets sur GitHub et Vercel
"""

import os
import subprocess
from pathlib import Path
from typing import Any

import httpx
from github import Github


class DeployerAgent:
    """Agent qui déploie les projets"""
    
    def __init__(self):
        self.name = "Deployer"
        self.version = "1.0.0"
        self.github = None
        
        # Initialiser GitHub si token disponible
        token = os.getenv("GITHUB_TOKEN")
        if token:
            self.github = Github(token)
    
    async def deploy_to_github(
        self,
        project_path: str,
        repo_name: str,
        private: bool = False,
    ) -> dict[str, Any]:
        """Pousse un projet vers GitHub"""
        
        if not self.github:
            return {"error": "GITHUB_TOKEN non configuré"}
        
        path = Path(project_path)
        if not path.exists():
            return {"error": "Projet introuvable"}
        
        try:
            # Créer ou récupérer le repo
            user = self.github.get_user()
            
            # Initialiser git si pas encore fait
            if not (path / ".git").exists():
                subprocess.run(["git", "init"], cwd=path, check=True)
            
            # Ajouter remote
            try:
                subprocess.run(
                    ["git", "remote", "add", "origin", f"git@github.com:{user.login}/{repo_name}.git"],
                    cwd=path,
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError:
                pass  # Remote existe déjà
            
            # Commit
            subprocess.run(["git", "add", "."], cwd=path, check=True)
            try:
                subprocess.run(
                    ["git", "commit", "-m", "Initial commit via ELECTRON AI"],
                    cwd=path,
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError:
                pass  # Rien à commit
            
            # Push
            subprocess.run(
                ["git", "push", "-u", "origin", "main"],
                cwd=path,
                env={**os.environ, "GIT_SSH_COMMAND": "ssh -o StrictHostKeyChecking=no"},
                check=True,
            )
            
            return {
                "status": "success",
                "repo": f"{user.login}/{repo_name}",
                "url": f"https://github.com/{user.login}/{repo_name}",
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def deploy_to_vercel(
        self,
        repo_url: str,
        project_id: str | None = None,
    ) -> dict[str, Any]:
        """Déploie sur Vercel"""
        
        token = os.getenv("VERCEL_TOKEN")
        if not token:
            return {"error": "VERCEL_TOKEN non configuré"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.vercel.com/v6/deployments",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "name": repo_url.split("/")[-1].replace(".git", ""),
                        "repo": repo_url,
                        "branch": "main",
                    },
                    timeout=30.0,
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "status": "success",
                        "url": data.get("url", data.get("deployment", {}).get("url")),
                    }
                else:
                    return {"error": response.text}
                    
        except Exception as e:
            return {"error": str(e)}
    
    async def deploy(
        self,
        project_path: str,
        repo_name: str,
    ) -> dict[str, Any]:
        """Déploiement complet (GitHub + Vercel)"""
        
        # GitHub
        github_result = await self.deploy_to_github(project_path, repo_name)
        
        if "error" in github_result:
            return github_result
        
        # Vercel
        vercel_result = await self.deploy_to_vercel(github_result["url"])
        
        return {
            "status": "success",
            "github": github_result,
            "vercel": vercel_result,
        }