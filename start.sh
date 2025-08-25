#!/bin/bash

# Kick Points Collector dla Linux/Mac

echo "🎯 Kick Points Collector - Uruchamianie"
echo "========================================"
echo

if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python nie jest zainstalowany lub nie jest w PATH!"
    echo
    echo "Proszę zainstalować Pythona:"
    echo "  - Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"
    echo "  - Fedora: sudo dnf install python3 python3-pip"
    echo "  - Arch: sudo pacman -S python python-pip"
    echo "  - macOS: brew install python3"
    echo
    echo "Możesz też uruchomić instalator:"
    echo "  python3 install.py"
    echo
    exit 1
fi

if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "✅ Znaleziono Python: $PYTHON_CMD"

if [ ! -f "config.json" ]; then
    echo "❌ Plik konfiguracyjny config.json nie istnieje!"
    echo
    echo "Uruchom kreator konfiguracji:"
    echo "  $PYTHON_CMD setup.py"
    echo
    exit 1
fi

if [ ! -f "main_improved.py" ]; then
    echo "❌ Plik main_improved.py nie istnieje!"
    echo
    exit 1
fi

echo "✅ Wszystkie pliki znalezione"
echo "🚀 Uruchamianie bota..."
echo
echo "Naciśnij Ctrl+C aby zatrzymać bota"
echo

$PYTHON_CMD main_improved.py

echo
echo "Bot został zatrzymany"