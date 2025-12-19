"""
Processador Incremental de Relatórios
Analisa PDFs em etapas e notifica progresso em tempo real
"""
import base64
import json
from pathlib import Path
from datetime import datetime
import hashlib
import asyncio

from app.database import SessionLocal
from app.models.relatorio import Relatorio
from app.services.websocket_manager import manager


class RelatorioProcessorIncremental:
    """Processa relatórios em etapas, notificando progresso"""
    
    def __init__(self, anthropic_client, modelo="claude-sonnet-4-20250514"):
        self.client = anthropic_client
        self.modelo = modelo
    
    async def processar_incremental(
        self,
        relatorio_id: int,
        pdf_path: Path,
        json_path: Path,
        content_type: str,
        user_id: int
    ):
        """
        Processa relatório em etapas, enviando atualizações via WebSocket
        
        Etapas:
        1. Extração básica (20%) - Nome, registro, especialidade
        2. Datas e CID (40%) - Datas e diagnósticos
        3. Resumo (60%) - Resumo clínico
        4. Detalhes (80%) - Recomendações e adaptações
        5. Finalização (100%) - Salvar tudo
        """
        
        try:
            # Ler arquivo
            with open(pdf_path, "rb") as f:
                file_content = f.read()
            
            file_base64 = base64.standard_b64encode(file_content).decode("utf-8")
            media_type = self._get_media_type(content_type)
            
            # ETAPA 1: Dados básicos do profissional (20%)
            await manager.notify_relatorio_progress(
                user_id, relatorio_id, "extracting_professional", 20
            )
            
            profissional_data = await self._extrair_profissional(
                file_base64, media_type, content_type
            )
            
            await self._atualizar_banco(relatorio_id, profissional_data)
            await manager.notify_relatorio_progress(
                user_id, relatorio_id, "professional_extracted", 20, profissional_data
            )
            
            # ETAPA 2: Datas e diagnósticos (40%)
            await manager.notify_relatorio_progress(
                user_id, relatorio_id, "extracting_diagnostics", 40
            )
            
            diagnostico_data = await self._extrair_diagnosticos(
                file_base64, media_type, content_type
            )
            
            await self._atualizar_banco(relatorio_id, diagnostico_data)
            await manager.notify_relatorio_progress(
                user_id, relatorio_id, "diagnostics_extracted", 40, diagnostico_data
            )
            
            # ETAPA 3: Resumo clínico (60%)
            await manager.notify_relatorio_progress(
                user_id, relatorio_id, "extracting_summary", 60
            )
            
            resumo_data = await self._extrair_resumo(
                file_base64, media_type, content_type
            )
            
            await self._atualizar_banco(relatorio_id, resumo_data)
            await manager.notify_relatorio_progress(
                user_id, relatorio_id, "summary_extracted", 60, resumo_data
            )
            
            # ETAPA 4: Recomendações e adaptações (80%)
            await manager.notify_relatorio_progress(
                user_id, relatorio_id, "extracting_recommendations", 80
            )
            
            recomendacoes_data = await self._extrair_recomendacoes(
                file_base64, media_type, content_type
            )
            
            await self._atualizar_banco(relatorio_id, recomendacoes_data)
            await manager.notify_relatorio_progress(
                user_id, relatorio_id, "recommendations_extracted", 80, recomendacoes_data
            )
            
            # ETAPA 5: Consolidar dados completos (100%)
            await manager.notify_relatorio_progress(
                user_id, relatorio_id, "finalizing", 90
            )
            
            # Juntar todos os dados
            dados_completos = {
                **profissional_data,
                **diagnostico_data,
                **resumo_data,
                **recomendacoes_data
            }
            
            # Salvar JSON completo
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(dados_completos, f, ensure_ascii=False, indent=2)
            
            await manager.notify_relatorio_progress(
                user_id, relatorio_id, "completed", 100, {"json_saved": True}
            )
            
            print(f"🎉 [INCREMENTAL] Relatório {relatorio_id} processado!")
            
        except Exception as e:
            print(f"❌ [INCREMENTAL] Erro: {e}")
            await manager.notify_relatorio_progress(
                user_id, relatorio_id, "error", 0, {"error": str(e)}
            )
    
    async def _extrair_profissional(self, file_base64, media_type, content_type):
        """Extrai apenas dados do profissional"""
        prompt = """Extraia APENAS as informações do profissional deste relatório.
        
Retorne JSON com:
{
    "tipo_laudo": "string",
    "profissional": {
        "nome": "string",
        "registro": "string", 
        "especialidade": "string"
    }
}

APENAS JSON, sem explicações."""
        
        response = await asyncio.to_thread(
            self._call_claude, file_base64, media_type, content_type, prompt
        )
        return self._parse_json(response)
    
    async def _extrair_diagnosticos(self, file_base64, media_type, content_type):
        """Extrai datas e diagnósticos"""
        prompt = """Extraia APENAS datas e diagnósticos deste relatório.

Retorne JSON com:
{
    "datas": {
        "emissao": "YYYY-MM-DD",
        "validade": "YYYY-MM-DD"
    },
    "diagnosticos": [{"cid": "string", "descricao": "string"}],
    "condicoes_identificadas": {
        "tea": false,
        "tdah": false,
        "dislexia": false,
        "discalculia": false,
        "deficiencia_intelectual": false
    }
}

APENAS JSON, sem explicações."""
        
        response = await asyncio.to_thread(
            self._call_claude, file_base64, media_type, content_type, prompt
        )
        return self._parse_json(response)
    
    async def _extrair_resumo(self, file_base64, media_type, content_type):
        """Extrai resumo clínico completo"""
        prompt = """Extraia APENAS o resumo clínico deste relatório.

Retorne JSON com:
{
    "resumo_clinico": "string (texto completo, sem truncar)"
}

IMPORTANTE: Inclua TODO o resumo, não corte o texto.
APENAS JSON, sem explicações."""
        
        response = await asyncio.to_thread(
            self._call_claude, file_base64, media_type, content_type, prompt
        )
        return self._parse_json(response)
    
    async def _extrair_recomendacoes(self, file_base64, media_type, content_type):
        """Extrai recomendações e adaptações"""
        prompt = """Extraia APENAS recomendações e adaptações deste relatório.

Retorne JSON com:
{
    "recomendacoes": ["string"],
    "adaptacoes_sugeridas": {
        "curriculares": "string",
        "avaliacao": "string",
        "ambiente": "string",
        "recursos": "string"
    },
    "acompanhamentos_indicados": [
        {"profissional": "string", "frequencia": "string"}
    ]
}

APENAS JSON, sem explicações."""
        
        response = await asyncio.to_thread(
            self._call_claude, file_base64, media_type, content_type, prompt
        )
        return self._parse_json(response)
    
    def _call_claude(self, file_base64, media_type, content_type, prompt):
        """Chama Claude de forma síncrona (para usar com asyncio.to_thread)"""
        message = self.client.messages.create(
            model=self.modelo,
            max_tokens=2000,  # Menor = mais rápido
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "document" if content_type == "application/pdf" else "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": file_base64,
                            },
                        },
                        {"type": "text", "text": prompt}
                    ],
                }
            ],
        )
        return message.content[0].text.strip()
    
    def _parse_json(self, text):
        """Parse JSON removendo markdown"""
        text = text.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(text)
        except:
            return {}
    
    def _get_media_type(self, content_type):
        """Retorna media type correto"""
        mapping = {
            "application/pdf": "application/pdf",
            "image/jpeg": "image/jpeg",
            "image/jpg": "image/jpeg",
            "image/png": "image/png",
            "image/webp": "image/webp"
        }
        return mapping.get(content_type, content_type)
    
    async def _atualizar_banco(self, relatorio_id, data):
        """Atualiza banco com dados parciais"""
        db = SessionLocal()
        try:
            relatorio = db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()
            if not relatorio:
                return
            
            # Atualizar campos conforme dados disponíveis
            if "tipo_laudo" in data:
                relatorio.tipo = data["tipo_laudo"][:100]
            
            if "profissional" in data:
                prof = data["profissional"]
                relatorio.profissional_nome = prof.get("nome", "")[:200]
                relatorio.profissional_registro = prof.get("registro", "")[:50]
                relatorio.profissional_especialidade = prof.get("especialidade", "")[:100]
            
            if "datas" in data:
                datas = data["datas"]
                if datas.get("emissao"):
                    try:
                        relatorio.data_emissao = datetime.strptime(datas["emissao"], "%Y-%m-%d")
                    except:
                        pass
            
            if "resumo_clinico" in data:
                relatorio.resumo = data["resumo_clinico"][:200]
            
            db.commit()
            
        except Exception as e:
            print(f"❌ Erro ao atualizar banco: {e}")
            db.rollback()
        finally:
            db.close()
