import socket
import threading

# Konfiguracja sieciowa serwera
HOST = '127.0.0.1' # Adres lokalny (localhost)
PORT = 55555       # Port, na którym nasłuchuje serwer

# Inicjalizacja gniazda sieciowego (AF_INET = IPv4, SOCK_STREAM = TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    """Funkcja wysyłająca wiadomość do wszystkich podłączonych klientów."""
    for client in clients:
        try:
            client.send(message)
        except:
            # W razie błędu przy wysyłaniu (np. klient nagle rozłączony)
            pass

def handle_client(client):
    """Funkcja obsługująca pojedynczego klienta w osobnym wątku."""
    while True:
        try:
            # Odbieranie wiadomości od klienta (max 1024 bajty)
            message = client.recv(1024)
            if message:
                broadcast(message)
            else:
                break
        except:
            # Obsługa błędu i usunięcie klienta z listy, jeśli się rozłączy
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} opuścił czat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive_connections():
    """Główna pętla serwera akceptująca nowe połączenia."""
    print(f"[START] Serwer nasłuchuje na {HOST}:{PORT}...")
    while True:
        # Akceptacja nowego połączenia od klienta
        client, address = server.accept()
        print(f"[POŁĄCZENIE] Połączono z adresem {str(address)}")

        # Prośba o podanie pseudonimu
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        
        # Zapisanie klienta i jego nicku do list
        nicknames.append(nickname)
        clients.append(client)

        print(f"[INFO] Pseudonim klienta to {nickname}")
        broadcast(f"{nickname} dołączył do czatu!\n".encode('utf-8'))
        client.send('Podłączono do serwera! Możesz zacząć pisać.\n'.encode('utf-8'))

        # Uruchomienie nowego wątku do obsługi tego konkretnego klienta
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Uruchomienie serwera
if __name__ == "__main__":
    receive_connections()