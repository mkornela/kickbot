@echo off
chcp 65001 >nul
title Kick Points Collector

echo.
echo Kick Points Collector
echo.

REM Sprawdzenie czy Python jest zainstalowany
python --version >nul 2>&1
if errorlevel 1 (
    echo Python nie jest zainstalowany lub nie jest w PATH!
    echo.
    echo Proszę zainstalować Pythona z https://www.python.org/downloads/
    echo Pamiętaj o zaznaczeniu "Add Python to PATH" podczas instalacji!
    echo.
    echo Możesz też uruchomić instalator:
    echo python install.py
    echo.
    pause
    exit /b 1
)

REM Sprawdzenie czy plik konfiguracyjny istnieje
if not exist "config.json" (
    echo Plik konfiguracyjny config.json nie istnieje!
    echo.
    echo Uruchamiam interaktywną konfigurację bota!
    python setup.py
    echo.
    pause
    exit /b 1
)

REM Sprawdzenie czy główny skrypt istnieje
if not exist "main.py" (
    echo Plik main.py nie istnieje!
    echo.
    pause
    exit /b 1
)

echo Wszystkie pliki znalezione
echo.
echo Uruchamianie bota...
cls
echo.
echo Naciśnij Ctrl+C aby zatrzymać bota
echo.

REM Uruchomienie bota
python main.py

echo.
echo Bot został zatrzymany
pause