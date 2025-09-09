@echo off
REM Script batch para executar a interface gráfica da ferramenta

echo ========================================
echo  INTERFACE GRAFICA - PORT SCANNER
echo ========================================
echo.

REM Verifica se Python está disponível
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo [+] Iniciando interface grafica...
    python gui_scanner.py
    goto :end
)

python3 --version >nul 2>&1
if %errorlevel% == 0 (
    echo [+] Iniciando interface grafica...
    python3 gui_scanner.py
    goto :end
)

py --version >nul 2>&1
if %errorlevel% == 0 (
    echo [+] Iniciando interface grafica...
    py gui_scanner.py
    goto :end
)

echo [!] ERRO: Python nao encontrado
echo Por favor, instale Python 3.6+ primeiro
pause

:end
