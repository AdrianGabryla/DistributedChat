import socket
import threading

clients = {}

def broadcast_to_room(message, room, sender_socket):
    """Wysyła wiadomość tylko do osób w tym samym pokoju."""
    for client, info in clients.items():
        if info['room'] == room and client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                del clients[client]

def handle_client(client_socket):
    # Domyślne ustawienia
    clients[client_socket] = {'nick': 'Anonim', 'room': 'ogolny'}
    
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg: break

            if msg.startswith("/nick "):
                old_nick = clients[client_socket]['nick']
                new_nick = msg.split(" ")[1]
                clients[client_socket]['nick'] = new_nick
                client_socket.send(f"Zmieniono nick na {new_nick}\n".encode())
            
            elif msg.startswith("/join "):
                new_room = msg.split(" ")[1]
                clients[client_socket]['room'] = new_room
                client_socket.send(f"Dołączasz do pokoju: {new_room}\n".encode())

            else:
                nick = clients[client_socket]['nick']
                room = clients[client_socket]['room']
                full_msg = f"[{room}] {nick}: {msg}"
                print(full_msg)
                broadcast_to_room(full_msg, room, client_socket)
        except:
            break

    del clients[client_socket]
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen()
    print("Serwer zarządzający chatem działa...")
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    start_server()