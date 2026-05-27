@echo off
title UPAO Link - Analizador de Encuesta (Modular)
color 0B
cls

echo ==========================================================
echo    🎓 INICIANDO REPORTE Y DASHBOARD - UPAO LINK 🎓
echo ==========================================================
echo.

:: 1. Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% == 0 goto python_installed

color 0C
echo [ERROR] No se pudo encontrar Python en el sistema.
echo Por favor, instala Python (v3.8 o superior) y marca la opcion
echo "Add Python to PATH" durante la instalacion.
echo.
pause
exit /b

:python_installed
:: 2. Instalar o actualizar dependencias
echo [1/3] Verificando e instalando librerias de requirements.txt...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% == 0 goto pip_success

echo.
echo [ADVERTENCIA] Hubo problemas instalando dependencias de forma directa.
echo Reintentando instalacion individual...
pip install pandas openpyxl streamlit plotly

:pip_success
echo.

:: 3. Ejecutar main.py para compilar el reporte estatico e iniciar Streamlit
echo [2/3] Generando Reporte Interactivo HTML y Lanzando Dashboard...
echo.
python main.py

echo.
echo [3/3] Proceso terminado.
echo Se ha generado el reporte premium interactivo en:
echo 'reports\Reporte_Interactivo_UPAO.html'
echo Puedes abrirlo directamente haciendo doble clic sobre el.
echo.
echo Tambien se ha iniciado el servidor local de Streamlit.
echo Si el navegador no se abrio automaticamente, puedes ingresar a:
echo http://localhost:8501
echo.
pause
