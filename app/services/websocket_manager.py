"""
Sistema de WebSocket para notificacoes em tempo real
Permite notificar o frontend conforme o processamento avanca
"""
from typing import Dict, Set
import json

class ConnectionManager:
    def __init__(self):
        # user_id/relatorio_id -> set of connections
        self.active_connections: Dict[int, Set] = {}
    
    async def connect(self, websocket, key_id: int):
        """Adiciona nova conexao WebSocket (key_id pode ser user_id ou relatorio_id)"""
        await websocket.accept()
        
        if key_id not in self.active_connections:
            self.active_connections[key_id] = set()
        
        self.active_connections[key_id].add(websocket)
        print(f"[WS] Conectado: key_id={key_id}")
    
    def disconnect(self, websocket, key_id: int):
        """Remove conexao WebSocket"""
        if key_id in self.active_connections:
            self.active_connections[key_id].discard(websocket)
            
            if not self.active_connections[key_id]:
                del self.active_connections[key_id]
        
        print(f"[WS] Desconectado: key_id={key_id}")
    
    async def send_personal_message(self, message: dict, key_id: int):
        """Envia mensagem para conexoes de um key_id especifico"""
        if key_id not in self.active_connections:
            return
        
        disconnected = set()
        for connection in self.active_connections[key_id]:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)
        
        # Remove conexoes mortas
        for conn in disconnected:
            self.active_connections[key_id].discard(conn)
    
    async def notify_relatorio_progress(
        self, 
        user_id: int, 
        relatorio_id: int, 
        stage: str, 
        progress: int,
        data: dict = None
    ):
        """Notifica progresso do processamento do relatorio (API antiga - mantida por compat)"""
        message = {
            "type": "relatorio_progress",
            "relatorio_id": relatorio_id,
            "stage": stage,
            "progress": progress,
            "data": data or {}
        }
        await self.send_personal_message(message, user_id)
    
    # ============================================
    # API NOVA - usada por relatorios_v2.py
    # Conecta por relatorio_id diretamente
    # ============================================
    
    async def send_progress(self, relatorio_id: int, progress: int, message: str):
        """Envia progresso para clientes conectados no relatorio_id"""
        payload = {
            "type": "progress",
            "progress": progress,
            "message": message
        }
        await self.send_personal_message(payload, relatorio_id)
    
    async def send_complete(self, relatorio_id: int, dados: dict):
        """Notifica conclusao do processamento"""
        payload = {
            "type": "complete",
            "progress": 100,
            "dados": dados
        }
        await self.send_personal_message(payload, relatorio_id)
    
    async def send_error(self, relatorio_id: int, error_message: str):
        """Notifica erro no processamento"""
        payload = {
            "type": "error",
            "message": error_message
        }
        await self.send_personal_message(payload, relatorio_id)


# Instancia global
manager = ConnectionManager()

# Alias para compatibilidade com relatorios_v2.py e outros imports
ws_manager = manager
