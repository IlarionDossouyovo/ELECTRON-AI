"""
Firebase Storage - Stockage et base de données pour ELECTRON AI
"""

import os
from typing import Any

import firebase_admin
from firebase_admin import credentials, firestore


class FirebaseStorage:
    """Gestion du stockage Firebase"""
    
    def __init__(self):
        self.db = None
        self._initialized = False
        
        # Vérifier si les credentials sont configurés
        if self._has_credentials():
            self._init_firebase()
    
    def _has_credentials(self) -> bool:
        """Vérifie si les credentials Firebase sont disponibles"""
        return bool(
            os.getenv("FIREBASE_PROJECT_ID")
            or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
    
    def _init_firebase(self):
        """Initialise Firebase"""
        try:
            # Utiliser les variables d'environnement
            project_id = os.getenv("FIREBASE_PROJECT_ID")
            
            if project_id:
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(
                    cred,
                    project_id=project_id
                )
                self.db = firestore.client()
                self._initialized = True
        except Exception as e:
            print(f"Firebase init error: {e}")
    
    async def save_project(self, project_data: dict[str, Any]) -> dict[str, Any]:
        """Sauvegarde un projet dans Firestore"""
        
        if not self.db:
            return {"error": "Firebase non initialisé"}
        
        try:
            doc_ref = self.db.collection("projects").document(project_data.get("name", "unnamed"))
            doc_ref.set({
                **project_data,
                "created_at": firestore.SERVER_TIMESTAMP,
                "updated_at": firestore.SERVER_TIMESTAMP,
            })
            
            return {
                "status": "success",
                "id": doc_ref.id,
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def get_project(self, project_name: str) -> dict[str, Any]:
        """Récupère un projet"""
        
        if not self.db:
            return {"error": "Firebase non initialisé"}
        
        try:
            doc = self.db.collection("projects").document(project_name).get()
            
            if doc.exists:
                return {"status": "success", "data": doc.to_dict()}
            else:
                return {"error": "Projet introuvable"}
        except Exception as e:
            return {"error": str(e)}
    
    async def list_projects(self) -> dict[str, Any]:
        """Liste tous les projets"""
        
        if not self.db:
            return {"error": "Firebase non initialisé"}
        
        try:
            docs = self.db.collection("projects").stream()
            projects = [doc.to_dict() for doc in docs]
            
            return {
                "status": "success",
                "count": len(projects),
                "projects": projects,
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def save_deployment(self, project_name: str, deployment_data: dict[str, Any]) -> dict[str, Any]:
        """Sauvegarde un déploiement"""
        
        if not self.db:
            return {"error": "Firebase non initialisé"}
        
        try:
            doc_ref = self.db.collection("projects").document(project_name).collection("deployments").document()
            doc_ref.set({
                **deployment_data,
                "created_at": firestore.SERVER_TIMESTAMP,
            })
            
            return {
                "status": "success",
                "id": doc_ref.id,
            }
        except Exception as e:
            return {"error": str(e)}