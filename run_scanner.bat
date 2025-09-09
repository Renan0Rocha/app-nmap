@echo off
REM Script batch para executar a ferramenta de varredura de portas no Windows
REM Tenta diferentes comandos Python até encontrar um que funcione

echo ========================================
echo  FERRAMENTA DE VARREDURA DE PORTAS
echo ========================================
echo.

REM Verifica se Python está disponível
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo [+] Python encontrado via 'python'
    set PYTHON_CMD=python
    goto :run_scanner
)

REM Tenta python3
python3 --version >nul 2>&1
if %errorlevel% == 0 (
    echo [+] Python encontrado via 'python3'
    set PYTHON_CMD=python3
    goto :run_scanner
)

REM Tenta py launcher
py --version >nul 2>&1
if %errorlevel% == 0 (
    echo [+] Python encontrado via 'py'
    set PYTHON_CMD=py
    goto :run_scanner
)

REM Python não encontrado
echo [!] ERRO: Python nao foi encontrado no sistema
echo.
echo Por favor, instale Python 3.6+ de uma das seguintes formas:
echo 1. Microsoft Store (recomendado para Windows 10/11)
echo 2. Site oficial: https://www.python.org/downloads/
echo 3. Anaconda: https://www.anaconda.com/products/individual
echo.
echo Certifique-se de marcar "Add Python to PATH" durante a instalacao
pause
exit /b 1

:run_scanner
echo [+] Executando ferramenta de varredura...
echo.

REM Executa o scanner com os argumentos passados
%PYTHON_CMD% port_scanner.py %*

REM Se não foram passados argumentos, mostra ajuda
if "%~1"=="" (
    echo.
    echo ========================================
    echo  EXEMPLOS DE USO
    echo ========================================
    echo.
    echo Varredura basica:
    echo   run_scanner.bat -t 192.168.1.1 -p 80,443
    echo.
    echo Varredura de rede:
    echo   run_scanner.bat -t 192.168.1.0/24 --common-ports
    echo.
    echo TCP e UDP:
    echo   run_scanner.bat -t 127.0.0.1 -p 53 --tcp --udp
    echo.
    echo Para ver todas as opcoes:
    echo   run_scanner.bat --help
    echo.
    echo Para interface grafica:
    echo   run_gui.bat
    echo.
)

pause
