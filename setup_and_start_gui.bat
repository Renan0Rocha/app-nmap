@echo off
title Port Scanner - GUI Interface
cd /d "%~dp0"

echo =============================================================
echo       🖼️ PORT SCANNER - INTERFACE DESKTOP GUI
echo =============================================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado! Instale Python 3.8+ antes de continuar.
    echo 📁 Download: https://python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python encontrado!
echo.

REM Verificar se virtualenv existe
if not exist "venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Erro ao criar ambiente virtual!
        pause
        exit /b 1
    )
)

REM Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências
echo 📋 Instalando dependências...
pip install --upgrade pip
pip install -r requirements.txt

REM Iniciar GUI
echo.
echo =============================================================
echo ✅ INICIANDO INTERFACE GUI...
echo 🖼️ A janela do aplicativo será aberta em instantes
echo =============================================================
echo.

python gui_scanner.py

echo.
echo GUI fechada.
pause
