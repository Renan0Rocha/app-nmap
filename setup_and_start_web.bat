@echo off
title Port Scanner - Web Interface
cd /d "%~dp0"

echo =============================================================
echo       🔍 PORT SCANNER - INTERFACE WEB
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
if exist "web_frontend\requirements_web.txt" (
    pip install -r web_frontend\requirements_web.txt
)

REM Preparar banco Django
echo 🗄️ Preparando banco de dados...
cd web_frontend
python manage.py makemigrations
python manage.py migrate

REM Iniciar servidor
echo.
echo =============================================================
echo ✅ INICIANDO SERVIDOR WEB...
echo 🌐 Interface disponível em: http://localhost:8000
echo 💡 Pressione Ctrl+C para parar o servidor
echo =============================================================
echo.

python manage.py runserver
pause
