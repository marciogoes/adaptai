# AdaptAI - Recriar Ambiente Virtual (Python 3.12)
Clear-Host

Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "  ADAPTAI - RECRIAR AMBIENTE VIRTUAL (Python 3.12)" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

Set-Location -Path $PSScriptRoot

# 1. Verificar Python 3.12
Write-Host "[1/8] Verificando Python 3.12..." -ForegroundColor Cyan
try {
    $pythonVersion = py -3.12 --version 2>&1
    Write-Host "[OK] Python 3.12 encontrado!" -ForegroundColor Green
    $pythonCmd = "py -3.12"
} catch {
    Write-Host "[AVISO] Python 3.12 não encontrado! Tentando Python padrão..." -ForegroundColor Yellow
    $pythonVersion = python --version 2>&1
    Write-Host $pythonVersion -ForegroundColor White
    $pythonCmd = "python"
}
Write-Host ""

# 2. Desativar venv antigo
Write-Host "[2/8] Desativando venv antigo (se ativo)..." -ForegroundColor Cyan
try {
    & deactivate 2>$null
} catch {}
Write-Host "[OK] Desativado!" -ForegroundColor Green
Write-Host ""

# 3. Remover venv antigo
Write-Host "[3/8] Removendo venv antigo..." -ForegroundColor Cyan
if (Test-Path "venv") {
    Write-Host "Removendo pasta venv..." -ForegroundColor Yellow
    Remove-Item -Path "venv" -Recurse -Force
    Write-Host "[OK] Venv antigo removido!" -ForegroundColor Green
} else {
    Write-Host "[OK] Nenhum venv antigo encontrado!" -ForegroundColor Green
}
Write-Host ""

# 4. Criar novo venv
Write-Host "[4/8] Criando novo venv com Python 3.12..." -ForegroundColor Cyan
if ($pythonCmd -eq "py -3.12") {
    & py -3.12 -m venv venv
} else {
    & python -m venv venv
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha ao criar venv!" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}
Write-Host "[OK] Venv criado com sucesso!" -ForegroundColor Green
Write-Host ""

# 5. Ativar venv
Write-Host "[5/8] Ativando novo venv..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1
Write-Host "[OK] Venv ativado!" -ForegroundColor Green
Write-Host ""

# 6. Atualizar pip
Write-Host "[6/8] Atualizando pip..." -ForegroundColor Cyan
& python -m pip install --upgrade pip --quiet
Write-Host "[OK] Pip atualizado!" -ForegroundColor Green
Write-Host ""

# 7. Instalar dependências
Write-Host "[7/8] Instalando dependências..." -ForegroundColor Cyan
Write-Host "(Isso pode levar alguns minutos...)" -ForegroundColor Yellow
& pip install fastapi uvicorn sqlalchemy pymysql python-dotenv python-jose[cryptography] passlib[bcrypt] python-multipart anthropic pydantic pydantic-settings --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha ao instalar dependências!" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}
Write-Host "[OK] Dependências instaladas!" -ForegroundColor Green
Write-Host ""

# 8. Verificar instalação
Write-Host "[8/8] Verificando instalação..." -ForegroundColor Cyan
& python --version
Write-Host ""
& pip list | Select-String "anthropic"
Write-Host ""

Write-Host "============================================================" -ForegroundColor Green
Write-Host "  AMBIENTE RECRIADO COM SUCESSO!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Iniciando servidor em 3 segundos..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Clear-Host
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  ADAPTAI BACKEND - INICIANDO..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Green
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "[!] Pressione CTRL+C para parar o servidor" -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

& uvicorn app.main:app --reload
