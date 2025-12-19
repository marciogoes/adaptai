
@router.post("/gerar-pei-de-relatorios")
async def gerar_pei_de_relatorios(
    data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    🎯 GERA PEI COMPLETO AUTOMATICAMENTE A PARTIR DOS RELATÓRIOS SALVOS
    
    Recebe lista de IDs de relatórios, carrega todos os dados e gera PEI completo com IA
    
    Body:
    {
        "student_id": int,
        "relatorio_ids": [1, 2, 3, ...]
    }
    """
    student_id = data.get("student_id")
    relatorio_ids = data.get("relatorio_ids", [])
    
    if not student_id:
        raise HTTPException(status_code=400, detail="student_id é obrigatório")
    
    if not relatorio_ids or len(relatorio_ids) == 0:
        raise HTTPException(
            status_code=400, 
            detail="Selecione pelo menos um relatório para gerar o PEI"
        )
    
    # Verificar se aluno existe
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    # Carregar relatórios
    relatorios = db.query(Relatorio).filter(
        Relatorio.id.in_(relatorio_ids),
        Relatorio.student_id == student_id
    ).all()
    
    if len(relatorios) == 0:
        raise HTTPException(
            status_code=404, 
            detail="Nenhum relatório encontrado com os IDs fornecidos"
        )
    
    # Compilar dados de todos os relatórios
    relatorios_dados = []
    for rel in relatorios:
        dados = rel.dados_extraidos
        
        # Carregar JSON completo se existir
        if isinstance(dados, dict) and dados.get("json_path"):
            json_file = RELATORIOS_DIR / dados["json_path"]
            if json_file.exists():
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        dados = json.load(f)
                except:
                    pass
        
        relatorios_dados.append({
            "id": rel.id,
            "tipo": rel.tipo,
            "profissional": {
                "nome": rel.profissional_nome,
                "especialidade": rel.profissional_especialidade,
                "registro": rel.profissional_registro
            },
            "data_emissao": rel.data_emissao.isoformat() if rel.data_emissao else None,
            "resumo": rel.resumo,
            "dados_completos": dados
        })
    
    # Chamar IA para gerar PEI
    client = get_anthropic_client()
    if not client:
        raise HTTPException(
            status_code=500,
            detail="Serviço de IA não disponível"
        )
    
    prompt = f"""Você é um especialista em educação inclusiva e está criando um Plano Educacional Individualizado (PEI) completo.

INFORMAÇÕES DO ALUNO:
- Nome: {student.name}
- Série/Ano: {student.grade_level or 'Não especificado'}

RELATÓRIOS DE TERAPIAS E ACOMPANHAMENTO ({len(relatorios_dados)} documentos):
{json.dumps(relatorios_dados, ensure_ascii=False, indent=2)}

Com base em TODOS os relatórios acima, gere um PEI COMPLETO e DETALHADO em formato JSON:

{{
    "diagnosticos": {{
        "tea": false,
        "tea_nivel": null,
        "tdah": false,
        "dislexia": false,
        "discalculia": false,
        "disgrafia": false,
        "deficiencia_visual": false,
        "deficiencia_auditiva": false,
        "deficiencia_intelectual": false,
        "deficiencia_fisica": false,
        "superdotacao": false,
        "outro": "",
        "outro_qual": ""
    }},
    "caracteristicas_gerais": "Parágrafo detalhado com características gerais do aluno, consolidando informações de TODOS os relatórios",
    "pontos_fortes": "Parágrafo detalhado com pontos fortes identificados pelos profissionais",
    "dificuldades": "Parágrafo detalhado com principais dificuldades identificadas",
    "adaptacoes_curriculares": "Parágrafo detalhado com adaptações curriculares específicas recomendadas pelos profissionais",
    "adaptacoes_avaliacao": "Parágrafo detalhado com adaptações para avaliações (tempo extra, formato, etc)",
    "adaptacoes_ambiente": "Parágrafo detalhado com adaptações de ambiente físico e social",
    "recursos_apoio": "Parágrafo detalhado com recursos e materiais de apoio necessários",
    "metas_curto_prazo": "Parágrafo detalhado com 3-5 metas concretas para 1-3 meses",
    "metas_medio_prazo": "Parágrafo detalhado com 3-5 metas concretas para 3-6 meses",
    "metas_longo_prazo": "Parágrafo detalhado com 3-5 metas concretas para o ano letivo",
    "estrategias_ensino": "Parágrafo detalhado com estratégias pedagógicas específicas",
    "estrategias_comunicacao": "Parágrafo detalhado com estratégias de comunicação (verbal, visual, etc)",
    "estrategias_comportamento": "Parágrafo detalhado com estratégias de manejo comportamental",
    "profissionais_apoio": "Lista de profissionais que devem acompanhar o aluno (psicólogo, fonoaudiólogo, etc)",
    "frequencia_acompanhamento": "Frequência recomendada para revisão do PEI e acompanhamentos",
    "observacoes": "Observações gerais importantes para a equipe escolar"
}}

INSTRUÇÕES IMPORTANTES:
1. Analise TODOS os relatórios e consolide as informações
2. Priorize recomendações que aparecem em múltiplos relatórios
3. Seja ESPECÍFICO e PRÁTICO - evite generalidades
4. Use linguagem acessível para professores
5. Foque em ações CONCRETAS e IMPLEMENTÁVEIS
6. Considere a realidade escolar brasileira
7. Marque os diagnósticos apenas se explicitamente mencionados
8. Nos parágrafos, seja detalhado (mínimo 3-4 linhas cada)
9. NUNCA use listas com bullet points ou números nos parágrafos - escreva texto corrido
10. Seja encorajador mas realista

Retorne APENAS o JSON, sem explicações adicionais."""

    try:
        print(f"🤖 Gerando PEI completo para {student.name} com {len(relatorios_dados)} relatórios...")
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )
        
        response_text = message.content[0].text.strip()
        
        # Limpar marcadores de código
        for marker in ["```json", "```"]:
            response_text = response_text.replace(marker, "")
        response_text = response_text.strip()
        
        try:
            pei_gerado = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao parsear JSON: {e}")
            pei_gerado = {
                "erro_parse": True,
                "texto_bruto": response_text,
                "mensagem": "Não foi possível estruturar o PEI automaticamente"
            }
        
        print(f"✅ PEI gerado com sucesso para {student.name}!")
        
        return {
            "success": True,
            "student_name": student.name,
            "relatorios_utilizados": len(relatorios_dados),
            "pei": pei_gerado
        }
        
    except Exception as e:
        print(f"❌ Erro ao gerar PEI: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar PEI com IA: {str(e)}"
        )
