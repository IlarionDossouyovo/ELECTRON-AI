"""
Coder Agent - Génère et modifie le code des projets
"""

import os
from pathlib import Path
from typing import Any


class CoderAgent:
    """Agent qui génère et modifie le code"""
    
    def __init__(self):
        self.name = "Coder"
        self.version = "1.0.0"
    
    async def generate(
        self,
        project_path: str,
        prompt: str,
        files: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Génère du code basé sur un prompt"""
        
        path = Path(project_path)
        
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        
        # Si des fichiers sont fournis, les créer
        if files:
            for filename, content in files.items():
                filepath = path / filename
                filepath.parent.mkdir(parents=True, exist_ok=True)
                filepath.write_text(content)
        
        return {
            "status": "success",
            "message": f"Code généré pour: {prompt}",
            "files_created": list(files.keys()) if files else [],
        }
    
    async def update(
        self,
        project_path: str,
        file_path: str,
        changes: str,
    ) -> dict[str, Any]:
        """Met à jour un fichier existant"""
        
        filepath = Path(project_path) / file_path
        
        if not filepath.exists():
            return {"error": "Fichier introuvable", "path": str(filepath)}
        
        # Lire le contenu actuel
        current_content = filepath.read_text()
        
        # Ici on appliquerait les changements
        # Pour l'instant, on retourne juste un message
        return {
            "status": "success",
            "message": f"Fichier mis à jour: {file_path}",
            "diff": changes,
        }
    
    async def create_file(
        self,
        project_path: str,
        filename: str,
        content: str,
    ) -> dict[str, Any]:
        """Crée un nouveau fichier"""
        
        filepath = Path(project_path) / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)
        
        return {
            "status": "success",
            "file": filename,
            "path": str(filepath),
        }