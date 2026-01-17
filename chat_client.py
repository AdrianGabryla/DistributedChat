import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 5555))

        self.root = tk.Tk()
        self.root.title("Chat")

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=5)
        
        tk.Label(self.top_frame, text="Nick:").pack(side=tk.LEFT)
        self.nick_entry = tk.Entry(self.top_frame, width=10)
        self.nick_entry.pack(side=tk.LEFT)
        tk.Button(self.top_frame, text="Ustaw", command=self.set_nick).pack(side=tk.LEFT)

        tk.Label(self.top_frame, text=" Pokój:").pack(side=tk.LEFT)
        self.room_entry = tk.Entry(self.top_frame, width=10)
        self.room_entry.pack(side=tk.LEFT)
        tk.Button(self.top_frame, text="Dołącz", command=self.join_room).pack(side=tk.LEFT)

        self.chat_area = scrolledtext.ScrolledText(self.root, width=50, height=20)
        self.chat_area.pack(padx=10, pady=10)

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(padx=10, pady=5, fill=tk.X)

        tk.Label(self.bottom_frame, text="Wiadomość:").pack(side=tk.LEFT) # Podpis
        
        self.msg_entry = tk.Entry(self.bottom_frame)
        self.msg_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.msg_entry.bind("<Return>", self.send_message)

        tk.Button(self.bottom_frame, text="Wyślij", command=lambda: self.send_message(None)).pack(side=tk.LEFT)

        threading.Thread(target=self.receive, daemon=True).start()
        self.root.mainloop()

    def set_nick(self):
        nick = self.nick_entry.get()
        if nick: self.client.send(f"/nick {nick}".encode())

    def join_room(self):
        room = self.room_entry.get()
        if room: self.client.send(f"/join {room}".encode())

    def send_message(self, event):
        message = self.msg_entry.get()
        self.chat_area.insert(tk.END, f"Ja: {message}\n")
        self.client.send(message.encode())
        self.msg_entry.delete(0, tk.END)

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                if message:
                    self.chat_area.insert(tk.END, message + "\n")
                    self.chat_area.yview(tk.END)
            except: break

if __name__ == "__main__":
    ChatClient()