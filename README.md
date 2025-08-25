# kick bot
Prosty bot do nabijanie punktów na platformie Kick, poprzez wysyłanie wiadomości na wybrane czaty!

## 🎯 Co zostało zrobione?
Przerobiłem oryginalny skrypt, aby był bardziej zrozumiały i łatwiejszy w użyciu.

## 📁 Nowe pliki

### 1. main.py - Poprawiony główny skrypt

Co zostało ulepszone:
- Lepsza struktura kodu - Kod podzielony na klasy i funkcje z jasnymi nazwami
- Szczegółowe komentarze - Każda funkcja i klasa jest opisana
- Lepsza obsługa błędów - Więcej informacji o błędach i ich przyczynach
- Walidacja konfiguracji - Skrypt sprawdza czy konfiguracja jest poprawna
- Typowanie - Użyte type hints dla lepszej czytelności

Kluczowe funkcje:
- KickPointsCollector - Główna klasa bota
- check_channel_status() - Sprawdzanie statusu kanału
- send_message() - Wysyłanie wiadomości na czat
- monitor_channel() - Monitorowanie pojedynczego kanału
- start_monitoring() - Uruchomienie monitorowania wszystkich kanałów

### 2. setup.py - Interaktywny kreator konfiguracji

Co robi:
- Przeprowadza użytkownika przez proces konfiguracji krok po kroku
- Wyjaśnia co każda opcja robi
- Waliduje dane wejściowe
- Umożliwia dodanie domyślnych emotek jednym kliknięciem
- Zapisuje konfigurację do pliku JSON

Kroki konfiguracji:
- Kanały do monitorowania - Podaj nazwy kanałów Kick.com
- Token autoryzacji - Wklej token z przeglądarki z instrukcją jak go zdobyć
- Czasy oczekiwania - Konfiguracja jak często bot ma wysyłać wiadomości
- Wiadomości/emotki - Wybór co bot ma wysyłać na czat

### 3. install.py - Automatyczny instalator

Co robi:
- Sprawdza czy Python jest zainstalowany
- Sprawdza czy Python jest w PATH
- Instaluje wymagane pakiety (cloudscraper)
- Testuje instalację
- Tworzy skróty na pulpicie (jeśli możliwe)
- Uruchamia kreator konfiguracji

Obsługa błędów:
- Jeśli Python nie jest zainstalowany - pokazuje jak go zainstalować
- Jeśli Python nie jest w PATH - pokazuje jak to naprawić
- Jeśli pip nie działa - pokazuje alternatywne rozwiązania

### 4. start_bot.bat i start_bot.sh - Uruchamiacze

Co robią:
- Sprawdzają wszystkie wymagania przed uruchomieniem
- Wyświetlają czytelne komunikaty o błędach
- Ułatwiają uruchomienie bota jednym kliknięciem