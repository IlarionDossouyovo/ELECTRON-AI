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
        """Pousse un projet vers GitHub via API"""
        
        if not self.github:
            return {"error": "GITHUB_TOKEN non configuré"}
        
        path = Path(project_path)
        if not path.exists():
            return {"error": "Projet introuvable"}
        
        try:
            import base64
            import httpx
            
            user = self.github.get_user()
            login = user.login
            
            # Créer le repo via API
            try:
                repo = self.github.get_repo(f"{login}/{repo_name}")
            except Exception:
                repo = user.create_repo(repo_name, private=private, auto_init=False)
            
            # Upload tous les fichiers via API
            files_uploaded = []
            repo_obj = self.github.get_repo(f"{login}/{repo_name}")
            
            for file_path in path.rglob("*"):
                if file_path.is_file() and not file_path.name.startswith("."):
                    rel_path = file_path.relative_to(path)
                    if "node_modules" in str(rel_path) or "__pycache__" in str(rel_path):
                        continue
                    
                    with open(file_path, "rb") as f:
                        content = base64.b64encode(f.read()).decode()
                    
                    try:
                        # Vérifier si le fichier existe déjà
                        existing = repo_obj.get_contents(str(rel_path))
                        if isinstance(existing, list):
                            existing = existing[0]
                        repo_obj.update_file(
                            str(rel_path),
                            f"Update {rel_path}",
                            content,
                            existing.sha
                        )
                    except Exception:
                        # Créer nouveau fichier
                        try:
                            repo_obj.create_file(
                                str(rel_path),
                                f"Add {rel_path}",
                                content,
                                branch="main"
                            )
                        except Exception as e2:
                            print(f"Skip {rel_path}: {e2}")
                    files_uploaded.append(str(rel_path))
            
            return {
                "url": repo.html_url,
                "files": len(files_uploaded),
                "repo": repo_name
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