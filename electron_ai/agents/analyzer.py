"""
Analyzer Agent - Analyse les projets et génère des rapports
"""

import os
from pathlib import Path
from typing import Any


class AnalyzerAgent:
    """Agent qui analyse les projets pour comprendre leur structure"""
    
    def __init__(self):
        self.name = "Analyzer"
        self.version = "1.0.0"
    
    async def analyze(self, project_path: str) -> dict[str, Any]:
        """Analyse un projet et retourne un rapport"""
        
        path = Path(project_path)
        
        if not path.exists():
            return {"error": "Projet introuvable", "path": project_path}
        
        # Analyse de la structure
        structure = self._analyze_structure(path)
        
        # Analyse des dépendances
        dependencies = self._analyze_dependencies(path)
        
        # Analyse du tech stack
        tech_stack = self._detect_tech_stack(path)
        
        return {
            "status": "success",
            "project_name": path.name,
            "structure": structure,
            "dependencies": dependencies,
            "tech_stack": tech_stack,
            "files_count": sum(1 for _ in path.rglob("*") if _.is_file()),
        }
    
    def _analyze_structure(self, path: Path) -> dict:
        """Analyse la structure des dossiers"""
        
        dirs = [d.name for d in path.iterdir() if d.is_dir() and not d.name.startswith(".")]
        files = [f.name for f in path.iterdir() if f.is_file() and not f.name.startswith(".")]
        
        return {"dirs": dirs, "root_files": files}
    
    def _analyze_dependencies(self, path: Path) -> dict:
        """Détecte les dépendances"""
        
        deps = {}
        
        # Python
        pyproject = path / "pyproject.toml"
        requirements = path / "requirements.txt"
        if pyproject.exists():
            deps["type"] = "python"
            deps["manager"] = "uv" if (path / "uv.lock").exists() else "pip"
        
        # Node.js
        package_json = path / "package.json"
        if package_json.exists():
            deps["type"] = "nodejs"
            deps["manager"] = "npm"
        
        return deps
    
    def _detect_tech_stack(self, path: Path) -> list[str]:
        """Détecte le tech stack"""
        
        stack = []
        
        # Python frameworks
        if (path / "fastapi").exists() or (path / "app.py").exists():
            stack.append("FastAPI")
        if (path / "django").exists():
            stack.append("Django")
        
        # Frontend
        if (path / "next.config.js").exists() or (path / "next.config.mjs").exists():
            stack.append("Next.js")
        if (path / "react").exists():
            stack.append("React")
        if (path / "vue").exists():
            stack.append("Vue.js")
        
        # Database
        if (path / "firebase.json").exists():
            stack.append("Firebase")
        
        return stack