"""
N8N Notifications - Envoie des notifications WhatsApp via N8N
"""

import os
from typing import Any

import httpx


class N8NNotifier:
    """Envoie des notifications via N8N (WhatsApp, Slack, Email, etc.)"""
    
    def __init__(self):
        self.base_url = os.getenv("N8N_URL", "")
        self.api_key = os.getenv("N8N_API_KEY", "")
        self.enabled = bool(self.base_url and self.api_key)
    
    async def notify(
        self,
        message: str,
        channel: str = "whatsapp",
        recipient: str | None = None,
    ) -> dict[str, Any]:
        """Envoie une notification"""
        
        if not self.enabled:
            return {"error": "N8N non configuré (N8N_URL et N8N_API_KEY)"}
        
        try:
            async with httpx.AsyncClient() as client:
                # Appel au webhook N8N
                response = await client.post(
                    f"{self.base_url}/webhook/{channel}",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "message": message,
                        "recipient": recipient,
                        "from": "ELECTRON AI",
                    },
                    timeout=30.0,
                )
                
                if response.status_code in (200, 201):
                    return {
                        "status": "success",
                        "channel": channel,
                        "message": message,
                    }
                else:
                    return {"error": response.text}
                    
        except Exception as e:
            return {"error": str(e)}
    
    async def notify_deployment(
        self,
        project_name: str,
        url: str,
        status: str = "success",
    ) -> dict[str, Any]:
        """Notifie un déploiement"""
        
        message = f"🚀 *Déploiement {project_name}*\n\n"
        
        if status == "success":
            message += f"✅ *Statut:* Succès\n🔗 *URL:* {url}\n\n"
        else:
            message += f"❌ *Statut:* Échec\n\n"
        
        message += "_Envoyé par ELECTRON AI_"
        
        return await self.notify(message, "whatsapp")
    
    async def notify_analysis(
        self,
        project_name: str,
        files_count: int,
        tech_stack: list[str],
    ) -> dict[str, Any]:
        """Notifie une analyse"""
        
        stack_str = ", ".join(tech_stack) if tech_stack else "Non détecté"
        
        message = f"🔍 *Analyse: {project_name}*\n\n"
        message += f"📁 *Fichiers:* {files_count}\n"
        message += f"🛠 *Tech:* {stack_str}\n\n"
        message += "_Envoyé par ELECTRON AI_"
        
        return await self.notify(message, "whatsapp")