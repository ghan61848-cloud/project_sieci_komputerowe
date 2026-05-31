import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import sys

HOST = '127.0.0.1'
PORT = 55555

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TWORZYMY TYLKO JEDNO GŁÓWNE OKNO
        self.root = tk.Tk()
        self.root.title("Logowanie do Czatu")
        self.root.geometry("350x180")
        self.root.resizable(False, False)
        
        # Co się stanie, gdy użytkownik zamknie okno 'X'
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Ramki na poszczególne widoki
        self.login_frame = None
        self.chat_frame = None
        
        # Odpalamy widok logowania na starcie
        self.setup_login_gui()
        
        # Uruchamiamy główną pętlę graficzną (uruchamiana tylko RAZ!)
        self.root.mainloop()

    def setup_login_gui(self):
        """Tworzy panel logowania wewnątrz głównego okna."""
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(self.login_frame, text="Witaj w aplikacji Czat!", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.login_frame, text="Wybierz swój pseudonim:").pack(pady=2)
        
        self.nick_entry = tk.Entry(self.login_frame, font=("Arial", 11), width=25)
        self.nick_entry.pack(pady=5)
        # Pozwala zalogować się używając klawisza Enter
        self.nick_entry.bind("<Return>", lambda event: self.connect_to_server()) 
        self.nick_entry.focus()
        
        tk.Button(self.login_frame, text="Dołącz do czatu", font=("Arial", 10, "bold"), 
                  command=self.connect_to_server, bg="#4CAF50", fg="white", padx=10).pack(pady=10)

    def connect_to_server(self):
        """Próba połączenia po podaniu nicku."""
        self.nickname = self.nick_entry.get().strip()
        
        if not self.nickname:
            messagebox.showwarning("Błąd", "Pseudonim nie może być pusty!")
            return
        
        try:
            self.client.connect((self.host, self.port))
        except ConnectionRefusedError:
            messagebox.showerror("Błąd połączenia", "Nie można połączyć się z serwerem.\nUpewnij się, że serwer jest włączony.")
            return # Zamiast zamykać program, pozwalamy spróbować ponownie
            
        # Zmiana widoku: niszczymy TYLKO panel logowania, główne okno zostaje!
        self.login_frame.destroy()
        
        # Zmieniamy parametry okna na takie pod czat
        self.root.geometry("500x600")
        self.root.resizable(True, True)
        self.root.title(f"Aplikacja Czat - Połączono jako: {self.nickname}")
        
        # Rysujemy panel czatu
        self.setup_main_gui()
        
        # Startujemy wątek do odbioru wiadomości
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    def setup_main_gui(self):
        """Tworzy panel czatu wewnątrz głównego okna."""
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)
        
        self.chat_area = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, font=("Arial", 11))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state='disabled')
        
        bottom_frame = tk.Frame(self.chat_frame)
        bottom_frame.pack(padx=10, pady=(0, 10), fill=tk.X)
        
        self.msg_entry = tk.Entry(bottom_frame, font=("Arial", 11))
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=4)
        self.msg_entry.bind("<Return>", lambda event: self.send_message())
        self.msg_entry.focus()
        
        send_button = tk.Button(bottom_frame, text="Wyślij", font=("Arial", 10, "bold"), 
                                command=self.send_message, bg="#2196F3", fg="white", width=10)
        send_button.pack(side=tk.RIGHT)

    def receive_messages(self):
        """Wątek działający w tle."""
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                elif message == '':
                    self.display_message("System: Połączenie z serwerem zostało zerwane.")
                    self.client.close()
                    break
                else:
                    self.display_message(message)
            except Exception:
                break

    def display_message(self, message):
        """Wrzucenie zadania do poprawnej pętli głównego okna."""
        clean_msg = message.strip()
        if clean_msg:
            # Teraz self.root.after ZAWSZE zadziała
            self.root.after(0, self._insert_message, clean_msg)

    def _insert_message(self, clean_msg):
        """Faktyczna modyfikacja widoku."""
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, clean_msg + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def send_message(self):
        """Wysyłanie na serwer."""
        text = self.msg_entry.get().strip()
        if text:
            if text == '/quit':
                self.on_closing()
                return
                
            self.msg_entry.delete(0, tk.END)
            try:
                message = f'{self.nickname}: {text}'
                self.client.send(message.encode('utf-8'))
            except Exception:
                self.display_message("System: Nie udało się wysłać wiadomości.")

    def on_closing(self):
        """Zamykanie programu."""
        try:
            self.client.close()
        except Exception:
            pass
        self.root.destroy()
        sys.exit()

if __name__ == "__main__":
    ChatClient(HOST, PORT)