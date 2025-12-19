"""
Endpoint WebSocket para notificações em tempo real
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.api.dependencies import get_current_active_user_ws
from app.services.websocket_manager import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = None
):
    """
    WebSocket endpoint para notificações em tempo real
    
    Uso: ws://localhost:8000/api/v1/ws?token=JWT_TOKEN
    """
    
    # Validar token e obter user_id
    try:
        # Extrair user_id do token
        from app.core.security import decode_access_token
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            await websocket.close(code=1008)
            return
        
        user_id = int(user_id)
        
    except Exception as e:
        print(f"❌ WebSocket auth error: {e}")
        await websocket.close(code=1008)
        return
    
    # Conectar
    await manager.connect(websocket, user_id)
    
    try:
        while True:
            # Manter conexão viva
            data = await websocket.receive_text()
            
            # Echo para manter vivo
            if data == "ping":
                await websocket.send_text("pong")
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        manager.disconnect(websocket, user_id)
