"""
Service para geração de materiais com IA
"""
import anthropic
import json
from app.core.config import settings


class MaterialGeracaoService:
    """Service para gerar materiais educacionais com IA"""
    
    def __init__(self):
        """Inicializa o cliente da Anthropic (lazy)"""
        self._client = None
        self.model = "claude-3-5-sonnet-20241022"
    
    @property
    def client(self):
        """Lazy initialization do cliente Anthropic"""
        if self._client is None:
            self._client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        return self._client
    
    def gerar_material_visual(self, titulo: str, conteudo: str, materia: str, serie: str, adaptacoes: list = None) -> dict:
        """
        Gera um material visual rico em HTML
        
        Args:
            titulo: Título do material
            conteudo: Descrição do que deve ser criado
            materia: Matéria (ex: Biologia, Matemática)
            serie: Série/nível (ex: 8º ano)
            adaptacoes: Lista de adaptações necessárias (TEA, TDAH, etc)
        
        Returns:
            dict com 'success', 'html' e 'tokens_used'
        """
        adaptacoes_text = ""
        if adaptacoes:
            adaptacoes_text = f"\n\nIMPORTANTE: Este material será usado por alunos com: {', '.join(adaptacoes)}. Adapte a linguagem e formato para ser mais acessível."
        
        prompt = f"""Crie um material educacional VISUAL e ATRATIVO sobre: {titulo}

MATÉRIA: {materia}
SÉRIE/NÍVEL: {serie}

CONTEÚDO SOLICITADO:
{conteudo}{adaptacoes_text}

IMPORTANTE - FORMATO DE SAÍDA:
- Retorne APENAS o conteúdo HTML (SEM as tags <html>, <head>, <body>)
- Use CSS inline para estilização
- Crie um conteúdo VISUALMENTE RICO e ATRATIVO

ESTRUTURA DO CONTEÚDO:
1. TÍTULO PRINCIPAL (grande, colorido, com gradiente)
2. INTRODUÇÃO VISUAL (box com cor de fundo, texto introdutório)
3. SEÇÕES BEM DEFINIDAS:
   - Cada seção com título colorido
   - Background diferente para cada seção
   - Boxes informativos coloridos
   - Exemplos práticos destacados
4. DIAGRAMAS/FLUXOGRAMAS em texto (use caracteres ▶, ►, →, ↓, •, ◆)
5. RESUMO FINAL em cards coloridos

ESTILO CSS INLINE:
- Use cores vibrantes e gradientes (ex: background: linear-gradient(135deg, #667eea 0%, #764ba2 100%))
- Cards com sombras (box-shadow)
- Use emojis e ícones quando apropriado
- Fonte grande e legível (min 16px)
- Espaçamento generoso (padding, margin)
- Bordas arredondadas (border-radius)
- Tipografia hierárquica (h1, h2, h3 bem definidos)
- Adicione hover effects sutis

EXEMPLO DE ESTRUTURA:
<div style="max-width: 800px; margin: 0 auto; font-family: 'Segoe UI', Arial, sans-serif;">
  <h1 style="font-size: 42px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 30px;">
    [TÍTULO]
  </h1>
  
  <div style="background: #f0f4ff; padding: 25px; border-radius: 15px; margin-bottom: 30px; border-left: 5px solid #667eea;">
    <p style="font-size: 18px; line-height: 1.8; color: #333;">
      [INTRODUÇÃO]
    </p>
  </div>
  
  <h2 style="color: #667eea; font-size: 32px; margin-top: 40px; margin-bottom: 20px;">
    📚 [SEÇÃO 1]
  </h2>
  
  <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 25px;">
    [CONTEÚDO DA SEÇÃO]
  </div>
  
  <!-- Mais seções... -->
</div>

NÃO inclua explicações, apenas o HTML puro e bem formatado."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            html_content = response.content[0].text.strip()
            
            # Remover markdown se houver
            html_content = html_content.replace("```html", "").replace("```", "").strip()
            
            return {
                "success": True,
                "html": html_content,
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def gerar_mapa_mental(self, titulo: str, conteudo: str, materia: str, serie: str, adaptacoes: list = None) -> dict:
        """
        Gera um mapa mental estruturado em JSON
        
        Args:
            titulo: Título do mapa mental
            conteudo: Descrição do que deve ser criado
            materia: Matéria
            serie: Série/nível
            adaptacoes: Lista de adaptações
        
        Returns:
            dict com 'success', 'json' e 'tokens_used'
        """
        adaptacoes_text = ""
        if adaptacoes:
            adaptacoes_text = f"\n\nADAPTAÇÕES: Simplifique para alunos com: {', '.join(adaptacoes)}"
        
        prompt = f"""Crie um mapa mental sobre: {titulo}

MATÉRIA: {materia}
SÉRIE: {serie}

CONTEÚDO:
{conteudo}{adaptacoes_text}

RETORNE APENAS UM JSON com esta estrutura exata:
{{
  "titulo": "Conceito Central",
  "cor_central": "#6366F1",
  "nos": [
    {{
      "id": "no1",
      "texto": "Conceito Principal 1",
      "cor": "#EF4444",
      "nivel": 1,
      "filhos": [
        {{
          "id": "no1_1",
          "texto": "Subconceito 1.1",
          "cor": "#FCA5A5",
          "nivel": 2,
          "filhos": []
        }}
      ]
    }}
  ]
}}

REGRAS IMPORTANTES:
1. O conceito central vai no "titulo"
2. Crie 3-5 nós principais (nivel: 1)
3. Cada nó principal pode ter 2-4 subnós (nivel: 2)
4. Máximo 20-25 nós no total
5. Use textos CURTOS (4-5 palavras máximo)
6. Use emojis apropriados nos textos
7. IDs únicos para cada nó (ex: no1, no1_1, no1_2)
8. Cores sugeridas:
   - Central: #6366F1 (azul/roxo)
   - Nível 1: #EF4444 (vermelho), #10B981 (verde), #F59E0B (laranja), #8B5CF6 (roxo), #EC4899 (rosa)
   - Nível 2: versões mais claras (#FCA5A5, #86EFAC, #FCD34D, #C4B5FD, #F9A8D4)

RETORNE APENAS O JSON, sem explicações ou markdown."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            json_text = response.content[0].text.strip()
            
            # Remover markdown se houver
            json_text = json_text.replace("```json", "").replace("```", "").strip()
            
            # Parse JSON
            try:
                mapa_json = json.loads(json_text)
            except json.JSONDecodeError as je:
                return {
                    "success": False,
                    "error": f"JSON inválido retornado pela IA: {str(je)}",
                    "raw_response": json_text
                }
            
            return {
                "success": True,
                "json": mapa_json,
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Instância global do service
material_service = MaterialGeracaoService()
