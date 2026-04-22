@echo off
echo ============================================
echo   WBI Dokumentations-Assistent (Server)
echo   Zugaenglich fuer alle im Netzwerk
echo ============================================
echo.
echo HINWEIS: Stelle sicher, dass in config.ini
echo          host = 0.0.0.0 gesetzt ist.
echo.
python --version >nul 2>&1
if errorlevel 1 (echo FEHLER: Python nicht gefunden. && pause && exit /b 1)
echo Pruefe und installiere Abhaengigkeiten...
pip install -r requirements.txt -q
echo.
echo Server laeuft. Druecke Strg+C zum Beenden.
echo.
python app.py
pause
