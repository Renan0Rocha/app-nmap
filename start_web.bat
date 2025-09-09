@echo off
title Port Scanner - Interface Web
color 0A

echo.
echo ========================================
echo    🌐 PORT SCANNER - INTERFACE WEB
echo ========================================
echo.
echo 📋 Iniciando servidor Django...
echo.

cd web_frontend

echo 🔍 Verificando configuração...
python manage.py check --deploy > nul 2>&1

echo 🚀 Iniciando servidor na porta 8000...
echo.
echo ┌─────────────────────────────────────┐
echo │  ✅ Servidor iniciado com sucesso!   │
echo │                                     │
echo │  🌐 Acesse: http://localhost:8000   │
echo │                                     │
echo │  💡 Para parar: Ctrl+C             │
echo └─────────────────────────────────────┘
echo.

python manage.py runserver 8000

echo.
echo 🔴 Servidor parado.
pause
