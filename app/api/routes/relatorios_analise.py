"""
Análise Consolidada de Relatórios com IA
Gera relatório temporal visual sobre a evolução do aluno
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
from datetime import datetime
from pathlib import Path

from app.database import get_db
from app.core.config import settings
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.models.student import Student
from app.models.relatorio import Relatorio

router = APIRouter(prefix="/relatorios", tags=["Relatórios - Análise Consolidada"])

# Diretório para salvar relatórios
RELATORIOS_DIR = Path(__file__).parent.parent.parent.parent / "storage" / "relatorios"

def get_anthropic_client():
    """Obtém cliente Anthropic"""
    try:
        from anthropic import Anthropic
        return Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    except Exception as e:
        print(f"[AVISO] Erro ao inicializar Anthropic: {e}")
        return None


@router.get("/student/{student_id}/analise-consolidada")
async def gerar_analise_consolidada(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🎨 ANÁLISE CONSOLIDADA VISUAL
    
    Agrega todos os relatórios do aluno e gera análise temporal com IA
    Retorna dados estruturados para visualização tipo Visual Law
    """
    
    # Verificar se aluno existe
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    # Buscar TODOS os relatórios do aluno
    relatorios = db.query(Relatorio).filter(
        Relatorio.student_id == student_id
    ).order_by(Relatorio.data_emissao.asc()).all()
    
    if not relatorios:
        raise HTTPException(
            status_code=404, 
            detail="Nenhum relatório encontrado para este aluno"
        )
    
    # Carregar dados completos de cada relatório
    relatorios_completos = []
    for rel in relatorios:
        dados = rel.dados_extraidos
        
        # Carregar JSON se existir
        if isinstance(dados, dict) and dados.get("json_path"):
            json_file = RELATORIOS_DIR / dados["json_path"]
            if json_file.exists():
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        dados = json.load(f)
                except:
                    pass
        
        relatorios_completos.append({
            "id": rel.id,
            "tipo": rel.tipo,
            "profissional": {
                "nome": rel.profissional_nome,
                "especialidade": rel.profissional_especialidade,
                "registro": rel.profissional_registro
            },
            "data_emissao": rel.data_emissao.isoformat() if rel.data_emissao else None,
            "resumo": rel.resumo,
            "dados_extraidos": dados
        })
    
    # Chamar IA para análise consolidada
    client = get_anthropic_client()
    if not client:
        # Retornar dados básicos sem análise IA
        return {
            "student_name": student.name,
            "total_relatorios": len(relatorios_completos),
            "relatorios": relatorios_completos,
            "analise_ia": None,
            "erro": "Cliente IA não disponível"
        }
    
    # Preparar dados para IA
    dados_para_ia = json.dumps(relatorios_completos, ensure_ascii=False, indent=2)
    
    prompt = f"""Analise esta jornada terapêutica do aluno {student.name}.

RELATÓRIOS ({len(relatorios_completos)} no total):
{dados_para_ia}

Gere uma análise consolidada VISUAL em JSON com:

{{
    "linha_do_tempo": [
        {{
            "data": "YYYY-MM-DD",
            "marco": "string (evento importante)",
            "profissional": "string",
            "destaque": "string (conquista ou preocupação)"
        }}
    ],
    "areas_desenvolvimento": {{
        "cognitiva": {{
            "nivel_atual": "string (baixo/médio/alto)",
            "evolucao": "string (estável/melhorando/retrocedendo)",
            "pontos_fortes": ["string"],
            "areas_atencao": ["string"],
            "cor": "green/yellow/red"
        }},
        "linguagem": {{...}},
        "motora": {{...}},
        "social_emocional": {{...}},
        "comportamental": {{...}}
    }},
    "diagnosticos_consolidados": [
        {{
            "condicao": "string",
            "confirmado": true/false,
            "nivel": "string",
            "primeiros_sinais": "YYYY-MM-DD",
            "evolucao": "string"
        }}
    ],
    "conquistas": [
        {{
            "area": "string",
            "descricao": "string",
            "data": "YYYY-MM-DD",
            "impacto": "alto/médio/baixo"
        }}
    ],
    "desafios_atuais": [
        {{
            "area": "string",
            "descricao": "string",
            "urgencia": "alta/média/baixa",
            "recomendacao": "string"
        }}
    ],
    "profissionais_envolvidos": [
        {{
            "nome": "string",
            "especialidade": "string",
            "periodo": "string",
            "foco_trabalho": "string"
        }}
    ],
    "recomendacoes_consolidadas": {{
        "curto_prazo": ["string"],
        "medio_prazo": ["string"],
        "longo_prazo": ["string"]
    }},
    "analise_progresso": {{
        "tendencia_geral": "positiva/estável/preocupante",
        "areas_melhoria": ["string"],
        "areas_atencao": ["string"],
        "perspectiva": "string (parágrafo sobre o futuro)"
    }},
    "indicadores_visuais": {{
        "progresso_geral": 0-100,
        "independencia": 0-100,
        "comunicacao": 0-100,
        "socializacao": 0-100,
        "aprendizado": 0-100
    }}
}}

IMPORTANTE: 
- Seja visual e objetivo
- Use cores (green/yellow/red) para facilitar interpretação
- Destaque conquistas e não só problemas
- Seja encorajador mas realista
- Foque na EVOLUÇÃO temporal
- Retorne APENAS o JSON, sem explicações
"""

    try:
        print(f"🤖 Gerando análise consolidada para {student.name}...")
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )
        
        response_text = message.content[0].text.strip()
        
        # Limpar markdown
        for marker in ["```json", "```"]:
            response_text = response_text.replace(marker, "")
        response_text = response_text.strip()
        
        try:
            analise_ia = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao parsear JSON da IA: {e}")
            analise_ia = {
                "erro": "Não foi possível estruturar a análise",
                "texto_bruto": response_text
            }
        
        print(f"✅ Análise consolidada gerada!")
        
        return {
            "student_name": student.name,
            "student_id": student_id,
            "total_relatorios": len(relatorios_completos),
            "periodo_analise": {
                "primeiro_relatorio": relatorios[0].data_emissao.isoformat() if relatorios[0].data_emissao else None,
                "ultimo_relatorio": relatorios[-1].data_emissao.isoformat() if relatorios[-1].data_emissao else None
            },
            "relatorios": relatorios_completos,
            "analise_ia": analise_ia,
            "gerado_em": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Erro ao gerar análise: {e}")
        return {
            "student_name": student.name,
            "total_relatorios": len(relatorios_completos),
            "relatorios": relatorios_completos,
            "analise_ia": None,
            "erro": str(e)
        }
