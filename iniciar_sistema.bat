@echo off
title Sistema Marroquineria - POS y Tienda Web
cd /d "%~dp0"

echo ========================================================
echo   Iniciando Sistema de Marroquineria (POS + E-Commerce)
echo ========================================================
echo.

:: Abrir navegador tras 2 segundos en segundo plano
start "" /b cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:8000/dashboard"

:: Ejecutar el servidor con el entorno virtual
"%~dp0venv\Scripts\python.exe" run.py

pause
