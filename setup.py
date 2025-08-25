#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive Setup

Interaktywny skrypt konfiguracyjny dla Kick Points Collector
Przeprowadzi Cię przez proces tworzenia pliku konfiguracyjnego

Autor: deem
"""

import json
import os
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "cloudscraper"])
os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Wyświetla nagłówek konfiguratora"""
    print("Kick Points Collector - Konfigurator Interaktywny")
    print("=" * 60)
    print("Ten skrypt pomoże Ci stworzyć plik konfiguracyjny dla bota.")
    print("Odpowiedz na poniższe pytania, aby skonfigurować bota.")
    print("=" * 60)
    print()


def get_channels():
    """
    Pobiera listę kanałów do monitorowania od użytkownika
    
    Returns:
        list: Lista nazw kanałów
    """
    print("\nKANAŁY DO MONITOROWANIA")
    print("-" * 40)
    print("Podaj nazwy kanałów Kick.com, które mają być monitorowane.")
    print("Bot będzie wysyłał wiadomości na te kanały, gdy będą aktywne.")
    print("Przykład: ['rybsonlol', 'xmerghani', 'banduracartel']")
    print()
    
    channels = []
    while True:
        channel = input("Podaj nazwę kanału (lub wciśnij Enter, aby zakończyć): ").strip()
        
        if not channel:
            if channels:
                break
            else:
                print("Musisz podać przynajmniej jeden kanał!")
                continue
        
        if channel.startswith('https://kick.com/'):
            channel = channel.replace('https://kick.com/', '')
        elif channel.startswith('http://kick.com/'):
            channel = channel.replace('http://kick.com/', '')
        
        channel = channel.rstrip('/')
        
        if channel:
            channels.append(channel)
            print(f"✅ Dodano kanał: {channel}")
    
    return channels


def get_authorization_token():
    """
    Pobiera token autoryzacji od użytkownika
    
    Returns:
        str: Token autoryzacji
    """
    print("\nTOKEN AUTORYZACJI")
    print("-" * 40)
    print("Token jest wymagany do wysyłania wiadomości na czacie Kick.com.")
    print()
    print("Jak zdobyć token:")
    print("1. Wejdź na dowolny stream na Kick.com")
    print("2. Otwórz narzędzia deweloperskie (F12)")
    print("3. Przejdź do zakładki 'Network' (Sieć)")
    print("4. Wyślij wiadomość na czacie")
    print("5. Znajdź request do 'kick.com/api/v2/messages/send/XXXXX'")
    print("6. W zakładce 'Headers' znajdź 'Authorization'")
    print("7. Skopiuj całą wartość (zaczynającą się od 'Bearer ')")
    print()
    
    while True:
        token = input("Wklej token autoryzacji: ").strip()
        
        if not token:
            print("Token jest wymagany!")
            continue
        
        if not token.startswith('Bearer '):
            print("Token musi zaczynać się od 'Bearer '!")
            print("   Przykład: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
            continue
        
        if len(token) < 20:
            print("Token wygląda na zbyt krótki. Sprawdź czy skopiowałeś cały token.")
            continue
        
        print("Token zaakceptowany")
        return token


def get_wait_times():
    """
    Pobiera konfigurację czasów oczekiwania od użytkownika
    
    Returns:
        dict: Konfiguracja czasów oczekiwania
    """
    print("\nKONFIGURACJA CZASÓW OCZEKIWANIA")
    print("-" * 40)
    print("Czasy oczekiwania kontrolują jak często bot wysyła wiadomości.")
    print("Dłuższe czasy = mniej ryzyka = wolniejsze zbieranie punktów")
    print("Krótsze czasy = więcej ryzyka = szybsze zbieranie punktów")
    print()
    
    wait_times = {}
    
    print("\nCZAS OCZEKIWANIA - STREAM AKTYWNY")
    print("Podaj zakres czasu oczekiwania (w sekundach) gdy stream jest aktywny.")
    print("Bot będzie czekał losową ilość czasu w tym zakresie przed wysłaniem kolejnej wiadomości.")
    print("Zalecane: 250-300 sekund (4-5 minut)")
    
    while True:
        try:
            min_time = int(input("Minimalny czas oczekiwania (sekundy): "))
            max_time = int(input("Maksymalny czas oczekiwania (sekundy): "))
            
            if min_time <= 0 or max_time <= 0:
                print("Czasy muszą być większe od 0!")
                continue
            
            if min_time >= max_time:
                print("Maksymalny czas musi być większy od minimalnego!")
                continue
            
            wait_times['livestream_active'] = {'min': min_time, 'max': max_time}
            print(f"Ustawiono zakres: {min_time}-{max_time} sekund")
            break
            
        except ValueError:
            print("Podaj liczby całkowite!")
    
    print("\nCZAS OCZEKIWANIA - STREAM NIEAKTYWNY")
    print("Podaj czas oczekiwania (w sekundach) gdy stream jest nieaktywny.")
    print("Bot będzie czekał ten czas przed ponownym sprawdzeniem statusu streamu.")
    print("Zalecane: 300 sekund (5 minut)")
    
    while True:
        try:
            inactive_time = int(input("Czas oczekiwania gdy stream nieaktywny (sekundy): "))
            
            if inactive_time <= 0:
                print("❌ Czas musi być większy od 0!")
                continue
            
            wait_times['livestream_inactive'] = inactive_time
            print(f"✅ Ustawiono czas: {inactive_time} sekund")
            break
            
        except ValueError:
            print("Podaj liczbę całkowitą!")
    
    # Czas oczekiwania przy błędzie
    print("\nCZAS OCZEKIWANIA - BŁĄD")
    print("Podaj czas oczekiwania (w sekundach) gdy wystąpi błąd.")
    print("Bot będzie czekał ten czas przed ponową próbą.")
    print("Zalecane: 180 sekund (3 minuty)")
    
    while True:
        try:
            error_time = int(input("Czas oczekiwania przy błędzie (sekundy): "))
            
            if error_time <= 0:
                print("Czas musi być większy od 0!")
                continue
            
            wait_times['error_wait'] = error_time
            print(f"Ustawiono czas: {error_time} sekund")
            break
            
        except ValueError:
            print("Podaj liczbę całkowitą!")
    
    return wait_times


def get_messages():
    """
    Pobiera listę wiadomości (emotek) od użytkownika
    
    Returns:
        list: Lista wiadomości/emotek
    """
    print("\nWIADOMOŚCI (EMOTKI)")
    print("-" * 40)
    print("Podaj wiadomości/emotki, które bot będzie wysyłał na czacie.")
    print("Możesz podać emotki w formacie [emote:ID:nazwa] lub zwykły tekst.")
    print("Przykłady:")
    print("  - [emote:1730752:emojiAngel]")
    print("  - [emote:1730753:emojiAngry]")
    print("  - Cześć!")
    print("  - Super stream!")
    print()
    print("Możesz też użyć opcji '1' aby załadować domyślny zestaw emotek.")
    print("Możesz też użyć opcji '2' aby wczytać emotki z pliku.")
    print()
    
    messages = []
    
    while True:
        print(f"\nAktualna liczba wiadomości: {len(messages)}")
        print("Opcje:")
        print("  1 - Dodaj domyślny zestaw emotek")
        print("  2 - Dodaj własną wiadomość/emotkę")
        print("  3 - Zakończ")
        
        choice = input("Wybierz opcję (1-3): ").strip()
        
        if choice == '1':
            default_emotes = [
                "[emote:1730752:emojiAngel]",
                "[emote:1730753:emojiAngry]",
                "[emote:1579033:emojiAstonished]",
                "[emote:1730754:emojiAwake]",
                "[emote:1579036:emojiBlowKiss]",
                "[emote:1730755:emojiBubbly]",
                "[emote:1730756:emojiCheerful]",
                "[emote:1730758:emojiClown]",
                "[emote:1730768:emojiDevil]",
                "[emote:1730772:emojiFire]",
                "[emote:1579054:emojiEyeRoll]",
                "[emote:1730767:emojiDead]",
                "[emote:1730765:emojiCute]",
                "[emote:1579045:emojiExcited]",
                "[emote:1579044:emojiEnraged]",
                "[emote:1730762:emojiCurious]",
                "[emote:1579040:emojiCrying]",
                "[emote:1730770:emojiDown]",
                "[emote:1730769:emojiDJ]",
                "[emote:1730761:emojiCry]",
                "[emote:1730760:emojiCrave]",
                "[emote:1579042:emojiDisguise]",
                "[emote:1579041:emojiDisappoint]",
                "[emote:1730759:emojiCool]",
                "[emote:3419634:emojiFlag]",
                "[emote:1730774:emojiGamer]",
                "[emote:1730775:emojiGlass]",
                "[emote:1730776:emojiGoofy]",
                "[emote:1730782:emojiGramps]",
                "[emote:1579046:emojiGrimacing]",
                "[emote:1730785:emojiGrin]",
                "[emote:1730786:emojiGrumpy]",
                "[emote:1730791:emojiLady]",
                "[emote:1730790:emojiKiss]",
                "[emote:1730789:emojiKing]",
                "[emote:4200908:emojiHydrate]",
                "[emote:1730788:emojiHmm]",
                "[emote:3419632:emojiHelmet]",
                "[emote:1579047:emojiHeartEyes]",
                "[emote:1730787:emojiHappy]",
                "[emote:1579050:emojiLaughing]",
                "[emote:1730792:emojiLoading]",
                "[emote:1730794:emojiLol]",
                "[emote:1730796:emojiMan]",
                "[emote:1579051:emojiMoneyEyes]",
                "[emote:1730798:emojiNo]",
                "[emote:1730799:emojiOof]",
                "[emote:1730800:emojiOooh]",
                "[emote:1579057:emojiSmiling]",
                "[emote:1730831:emojiWink]",
                "[emote:1579062:emojiVomiting]",
                "[emote:1579055:emojiSmerking]",
                "[emote:1730827:emojiSmart]",
                "[emote:3419630:emojiTire]",
                "[emote:1730825:emojiSleep]",
                "[emote:1730807:emojiShocked]",
                "[emote:1579059:emojiSwearing]",
                "[emote:1579058:emojiStarEyes]",
                "[emote:1730803:emojiRich]",
                "[emote:1579052:emojiPleading]",
                "[emote:1730830:emojiStare]",
                "[emote:1730829:emojiSorry]",
                "[emote:1730802:emojiOuch]",
                "[emote:1579038:emojiXEyes]",
                "[emote:1730834:emojiYay]",
                "[emote:1730835:emojiYes]",
                "[emote:1730839:emojiYuh]",
                "[emote:1730840:emojiYum]"
            ]
            
            messages.extend(default_emotes)
            print(f"✅ Dodano {len(default_emotes)} domyślnych emotek")
            
        elif choice == '2':
            # Dodanie własnej wiadomości
            message = input("Podaj wiadomość/emotkę: ").strip()
            if message:
                messages.append(message)
                print(f"Dodano wiadomość: {message}")
            else:
                print("Wiadomość nie może być pusta!")
                
        elif choice == '3':
            if messages:
                break
            else:
                print("Musisz dodać przynajmniej jedną wiadomość!")
                
        else:
            print("Nieprawidłowa opcja!")
    
    return messages


def save_config(config, filename='config.json'):
    """
    Zapisuje konfigurację do pliku JSON
    
    Args:
        config (dict): Konfiguracja do zapisania
        filename (str): Nazwa pliku
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"\nKonfiguracja została zapisana w pliku: {filename}")
    except Exception as e:
        print(f"\nBłąd zapisu konfiguracji: {e}")
        sys.exit(1)


def show_config_summary(config):
    """
    Wyświetla podsumowanie konfiguracji
    
    Args:
        config (dict): Konfiguracja do wyświetlenia
    """
    print("\n" + "=" * 60)
    print("PODSUMOWANIE KONFIGURACJI")
    print("=" * 60)
    
    print(f"\n📺 Kanały do monitorowania ({len(config['channels'])}):")
    for i, channel in enumerate(config['channels'], 1):
        print(f"   {i}. {channel}")
    
    print(f"\n⏰ Czasy oczekiwania:")
    print(f"   Stream aktywny: {config['wait_times']['livestream_active']['min']}-{config['wait_times']['livestream_active']['max']} sekund")
    print(f"   Stream nieaktywny: {config['wait_times']['livestream_inactive']} sekund")
    print(f"   Przy błędzie: {config['wait_times']['error_wait']} sekund")
    
    print(f"\nWiadomości (emotki): {len(config['messages'])}")
    print("   Pierwsze 5 wiadomości:")
    for i, message in enumerate(config['messages'][:5], 1):
        print(f"   {i}. {message}")
    if len(config['messages']) > 5:
        print(f"   ... i {len(config['messages']) - 5} więcej")
    
    print(f"\nToken autoryzacji: {config['authorization'][:50]}...")
    print("\n" + "=" * 60)


def main():
    """
    Główna funkcja konfiguratora
    """
    print_header()
    
    config = {
        'channels': get_channels(),
        'authorization': get_authorization_token(),
        'wait_times': get_wait_times(),
        'messages': get_messages()
    }
    
    show_config_summary(config)
    
    save_config(config)
    
    print("\n🎉 Konfiguracja zakończona pomyślnie!")
    print("Możesz teraz uruchomić bota komendą: python main.py")
    print("\n⚠️ UWAGA:")
    print("   - Używaj bota odpowiedzialnie i zgodnie z regulaminem Kick.com")
    print("   - Nie nadużywaj bota - może to prowadzić do zablokowania konta")
    print("   - Zalecane są konserwatywne ustawienia czasów oczekiwania")


if __name__ == "__main__":
    main()