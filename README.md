# Wielowątkowy Czat TCP z GUI

Prosty komunikator oparty na architekturze klient-serwer. Serwer wielowątkowo (`threading`) zarządza połączeniami i rozsyła wiadomości. Klient posiada interfejs graficzny (`Tkinter`), który dzięki asynchronicznemu działaniu w tle, nie zacina się przy odbieraniu danych z sieci. Do działania wystarczy standardowy Python (bez użycia `pip`).

 Jak uruchomić projekt

Dla testów wszystkie kroki wykonaj lokalnie (host `127.0.0.1` w kodzie).

1. Start Serwera (Terminal)
Otwórz terminal w folderze z projektem i wpisz:
```bash
python serwer.py
2. Start Klienta (GUI):
Otwórz nowe, osobne okno terminala i wpisz:

```bash
python klient.py
(Pojawi się okno. Wpisz pseudonim i kliknij "Dołącz do czatu")

można przetestować rozmowę z samym sobą, Otwórz kolejny, trzeci terminal i uruchom ponownie python klient.py
