import socket
import threading


HOST = '127.0.0.1' 
PORT = 55555       


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

            pass

def handle_client(client):
    """Funkcja obsługująca pojedynczego klienta w osobnym wątku."""
    while True:
        try:

            message = client.recv(1024)
            if message:
                broadcast(message)
            else:
                break
        except:

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

        client, address = server.accept()
        print(f"[POŁĄCZENIE] Połączono z adresem {str(address)}")


        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        

        nicknames.append(nickname)
        clients.append(client)

        print(f"[INFO] Pseudonim klienta to {nickname}")
        broadcast(f"{nickname} dołączył do czatu!\n".encode('utf-8'))
        client.send('Podłączono do serwera! Możesz zacząć pisać.\n'.encode('utf-8'))


        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive_connections()
