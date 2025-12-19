"""
Sistema de WebSocket para notificações em tempo real
Permite notificar o frontend conforme o processamento avança
"""
from typing import Dict, Set
import json

class ConnectionManager:
    def __init__(self):
        # user_id -> set of connections
        self.active_connections: Dict[int, Set] = {}
    
    async def connect(self, websocket, user_id: int):
        """Adiciona nova conexão WebSocket"""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        
        self.active_connections[user_id].add(websocket)
        print(f"✅ WebSocket conectado: User {user_id}")
    
    def disconnect(self, websocket, user_id: int):
        """Remove conexão WebSocket"""
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        
        print(f"❌ WebSocket desconectado: User {user_id}")
    
    async def send_personal_message(self, message: dict, user_id: int):
        """Envia mensagem para um usuário específico"""
        if user_id not in self.active_connections:
            return
        
        disconnected = set()
        for connection in self.active_connections[user_id]:
            try:
                await connection.send_json(message)
            except:
                disconnected.add(connection)
        
        # Remove conexões mortas
        for conn in disconnected:
            self.active_connections[user_id].discard(conn)
    
    async def notify_relatorio_progress(
        self, 
        user_id: int, 
        relatorio_id: int, 
        stage: str, 
        progress: int,
        data: dict = None
    ):
        """Notifica progresso do processamento do relatório"""
        message = {
            "type": "relatorio_progress",
            "relatorio_id": relatorio_id,
            "stage": stage,
            "progress": progress,
            "data": data or {}
        }
        await self.send_personal_message(message, user_id)

# Instância global
manager = ConnectionManager()
