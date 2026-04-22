@echo off
echo ============================================
echo   WBI Dokumentations-Assistent (Lokal)
echo ============================================
echo.
python --version >nul 2>&1
if errorlevel 1 (echo FEHLER: Python nicht gefunden. && pause && exit /b 1)
echo Pruefe und installiere Abhaengigkeiten...
pip install -r requirements.txt -q
echo.
echo Starte Server auf http://localhost:5000
python app.py
pause
