"""
Utilitários para gerenciamento de arquivos de storage dos materiais.
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Diretório base de storage
STORAGE_BASE_DIR = Path(__file__).parent.parent.parent / "storage" / "materiais"

def ensure_storage_dir():
    """Garante que o diretório de storage existe."""
    STORAGE_BASE_DIR.mkdir(parents=True, exist_ok=True)

def get_material_file_path(material_id: int, tipo: str) -> str:
    """
    Retorna o caminho do arquivo para um material.
    
    Args:
        material_id: ID do material
        tipo: Tipo do material (VISUAL, MAPA_MENTAL, etc)
    
    Returns:
        Caminho relativo do arquivo (ex: "123_visual.html")
    """
    extensao = "html" if tipo == "VISUAL" else "json"
    return f"{material_id}_{tipo.lower()}.{extensao}"

def salvar_conteudo_material(material_id: int, tipo: str, conteudo: str) -> str:
    """
    Salva o conteúdo de um material em arquivo.
    
    Args:
        material_id: ID do material
        tipo: Tipo do material
        conteudo: Conteúdo HTML ou JSON (como string)
    
    Returns:
        Caminho relativo do arquivo salvo
    """
    ensure_storage_dir()
    
    arquivo_path = get_material_file_path(material_id, tipo)
    arquivo_completo = STORAGE_BASE_DIR / arquivo_path
    
    # Salvar arquivo
    with open(arquivo_completo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"💾 Arquivo salvo: {arquivo_completo}")
    return arquivo_path

def ler_conteudo_material(arquivo_path: str) -> Optional[str]:
    """
    Lê o conteúdo de um material do arquivo.
    
    Args:
        arquivo_path: Caminho relativo do arquivo
    
    Returns:
        Conteúdo do arquivo ou None se não encontrado
    """
    arquivo_completo = STORAGE_BASE_DIR / arquivo_path
    
    if not arquivo_completo.exists():
        print(f"⚠️ Arquivo não encontrado: {arquivo_completo}")
        return None
    
    with open(arquivo_completo, 'r', encoding='utf-8') as f:
        return f.read()

def deletar_arquivo_material(arquivo_path: str) -> bool:
    """
    Deleta o arquivo de um material.
    
    Args:
        arquivo_path: Caminho relativo do arquivo
    
    Returns:
        True se deletou com sucesso, False caso contrário
    """
    arquivo_completo = STORAGE_BASE_DIR / arquivo_path
    
    if arquivo_completo.exists():
        arquivo_completo.unlink()
        print(f"🗑️ Arquivo deletado: {arquivo_completo}")
        return True
    
    return False

def verificar_arquivo_existe(arquivo_path: str) -> bool:
    """
    Verifica se o arquivo de um material existe.
    
    Args:
        arquivo_path: Caminho relativo do arquivo
    
    Returns:
        True se o arquivo existe, False caso contrário
    """
    arquivo_completo = STORAGE_BASE_DIR / arquivo_path
    return arquivo_completo.exists()
