#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ten skrypt automatycznie zbiera punkty na Kick.com poprzez wysyłanie emotek na podanych kanałach, gdy są aktywne.

Poprawiona wersja oryginalnego skryptu by blazejszhxk ( https://github.com/blazejszhxk/kick-auto-points-collector )

Autor: deem
"""

import time
import random
import json
import threading
import os
import sys
from typing import Dict, List, Tuple, Optional
import cloudscraper


class KickPointsCollector:
    """
    Główna klasa do automatycznego zbierania punktów na Kick.com
    """
    
    def __init__(self, config_path: str = 'config.json'):
        """
        Inicjalizacja kolektora punktów
        
        Args:
            config_path (str): Ścieżka do pliku konfiguracyjnego
        """
        self.config_path = config_path
        self.config = self.load_config()
        self.scraper = cloudscraper.create_scraper()
        
    def load_config(self) -> Dict:
        """
        Ładuje konfigurację z pliku JSON
        
        Returns:
            Dict: Załadowana konfiguracja
            
        Raises:
            FileNotFoundError: Jeśli plik konfiguracyjny nie istnieje
            json.JSONDecodeError: Jeśli plik konfiguracyjny jest nieprawidłowy
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.validate_config(config)
            return config
            
        except FileNotFoundError:
            print(f"BŁĄD: Plik konfiguracyjny '{self.config_path}' nie został znaleziony!")
            print("Użyj 'python setup.py' aby stworzyć konfigurację interaktywnie.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"BŁĄD: Nieprawidłowy format pliku konfiguracyjnego: {e}")
            sys.exit(1)
    
    def validate_config(self, config: Dict) -> None:
        """
        Waliduje konfigurację i sprawdza wymagane pola
        
        Args:
            config (Dict): Konfiguracja do walidacji
            
        Raises:
            ValueError: Jeśli konfiguracja jest nieprawidłowa
        """
        required_fields = {
            'channels': list,
            'wait_times': dict,
            'authorization': str,
            'messages': list
        }
        
        for field, field_type in required_fields.items():
            if field not in config:
                raise ValueError(f"Brak wymaganego pola w konfiguracji: '{field}'")
            if not isinstance(config[field], field_type):
                raise ValueError(f"Pole '{field}' musi być typu {field_type.__name__}")
        
        wait_times_required = ['livestream_active', 'livestream_inactive', 'error_wait']
        for field in wait_times_required:
            if field not in config['wait_times']:
                raise ValueError(f"Brak wymaganego pola w wait_times: '{field}'")
        
        livestream_active_required = ['min', 'max']
        for field in livestream_active_required:
            if field not in config['wait_times']['livestream_active']:
                raise ValueError(f"Brak wymaganego pola w livestream_active: '{field}'")
        
        if not config['channels']:
            raise ValueError("Lista kanałów nie może być pusta")
        if not config['messages']:
            raise ValueError("Lista wiadomości nie może być pusta")
        
        if not config['authorization'].startswith('Bearer '):
            raise ValueError("Token autoryzacji musi zaczynać się od 'Bearer '")

    def check_channel_status(self, channel_name: str) -> Tuple[bool, Optional[str]]:
        """
        Sprawdza status kanału i wysyła wiadomość jeśli stream jest aktywny
        
        Args:
            channel_name (str): Nazwa kanału do sprawdzenia
            
        Returns:
            Tuple[bool, Optional[str]]: (czy wiadomość została wysłana, wysłana wiadomość)
        """
        try:
            channel_url = f"https://kick.com/api/v2/channels/{channel_name}"
            channel_response = self.scraper.get(channel_url)
            channel_data = channel_response.json()
            
            if channel_data.get("livestream") is None:
                return False, None
            
            chatroom_id = channel_data.get("chatroom", {}).get("id")
            if not chatroom_id:
                return False, None
            
            return self.send_message(chatroom_id)
            
        except Exception as e:
            current_time = time.strftime("%H:%M:%S", time.localtime())
            print(f"[{current_time}] BŁĄD podczas sprawdzania statusu kanału {channel_name}: {str(e)}")
            return False, None

    def send_message(self, chatroom_id: str) -> Tuple[bool, Optional[str]]:
        """
        Wysyła wiadomość na czat
        
        Args:
            chatroom_id (str): ID czatu
            
        Returns:
            Tuple[bool, Optional[str]]: (czy wiadomość została wysłana, wysłana wiadomość)
        """
        try:
            message_url = f"https://kick.com/api/v2/messages/send/{chatroom_id}"
            
            random_message = random.choice(self.config["messages"])
            
            message_ref = str(random.randint(1000000000000, 9999999999999))
            
            payload = {
                "content": random_message,
                "type": "message",
                "message_ref": message_ref
            }
            
            headers = {
                "Authorization": self.config["authorization"],
                "Content-Type": "application/json"
            }
            
            response = self.scraper.post(message_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                return True, random_message
            else:
                current_time = time.strftime("%H:%M:%S", time.localtime())
                print(f"[{current_time}] BŁĄD: Kod odpowiedzi {response.status_code} dla wiadomości: {random_message}")
                return False, None
                
        except Exception as e:
            current_time = time.strftime("%H:%M:%S", time.localtime())
            print(f"[{current_time}] BŁĄD podczas wysyłania wiadomości: {str(e)}")
            return False, None

    def monitor_channel(self, channel_name: str) -> None:
        """
        Monitoruje pojedynczy kanał w nieskończonej pętli
        
        Args:
            channel_name (str): Nazwa kanału do monitorowania
        """
        print(f"Rozpoczynam monitorowanie kanału: {channel_name}")
        
        while True:
            try:
                message_sent, random_message = self.check_channel_status(channel_name)

                if message_sent:
                    wait_time = random.randint(
                        self.config["wait_times"]["livestream_active"]["min"], 
                        self.config["wait_times"]["livestream_active"]["max"]
                    )
                    current_time = time.strftime("%H:%M:%S", time.localtime())
                    print(f"[{current_time}] Wysłano do {channel_name}: {random_message} | Czekam {wait_time}s")
                else:
                    wait_time = self.config["wait_times"]["livestream_inactive"]
                    current_time = time.strftime("%H:%M:%S", time.localtime())
                    print(f"[{current_time}] ⏸ {channel_name} - stream nieaktywny | Czekam {wait_time}s")
                
                time.sleep(wait_time)
                
            except Exception as e:
                wait_time = self.config["wait_times"]["error_wait"]
                current_time = time.strftime("%H:%M:%S", time.localtime())
                print(f"[{current_time}] BŁĄD w monitorowaniu kanału {channel_name}: {str(e)} | Czekam {wait_time}s")
                time.sleep(wait_time)

    def start_monitoring(self) -> None:
        """
        Rozpoczyna monitorowanie wszystkich kanałów w osobnych wątkach
        """
        channels = self.config["channels"]
        
        if not channels:
            print("BŁĄD: Brak kanałów do monitorowania w konfiguracji!")
            return
        
        print(f"Rozpoczynam monitorowanie {len(channels)} kanałów...")
        print("Naciśnij Ctrl+C aby zatrzymać program")
        print("=" * 60)
        
        threads = []
        for channel_name in channels:
            thread = threading.Thread(target=self.monitor_channel, args=(channel_name,), daemon=True)
            threads.append(thread)
            thread.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n" + "=" * 60)
            print("Zatrzymywanie programu...")
            print("Dziękujemy za użycie Kick Points Collector!")


def main():
    """
    Główna funkcja programu
    """
    try:
        print("Kick.com Auto Points Collector")
        print("=" * 60)
        
        collector = KickPointsCollector()
        collector.start_monitoring()
        
    except Exception as e:
        print(f"BŁĄD KRYTYCZNY: {str(e)}")
        print("Sprawdź logi i spróbuj ponownie.")
        sys.exit(1)


if __name__ == "__main__":
    main()