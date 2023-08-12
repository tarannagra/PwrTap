
# Built in modules

import socket
import threading
import tomllib
import logging

# External modules
from pystyle import (
    Write,
    Colors,
)

# Local modules
from lib.design import Help

class Client:
    def __init__(self) -> None:
        self.data = tomllib.load(open('conf.toml', 'rb'))

        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

        self.host = self.data["client"]["host"]
        self.port = self.data["client"]["port"]

    def connect(self) -> None:
        try:
            self.client.connect((self.host, self.port))
        except socket.error:
            print(f"[E] Cannot connect to {self.host}:{self.port}")
            exit(1)
        
        print(f"Connected to {self.host}:{self.port}")
        
    def send(self, content: str) -> None:
        content = content.encode()
        self.client.send(content)

    def receive(self):
        while True:
            data = self.client.recv(4096)
            if not data:
                print("Disconnected from the server.")
                exit(0)
            print(f"Received: {data.decode()}")

    def input_thread(self):
        while True:
            to_send = input("> ")
            if to_send == "help" or to_send == "?":
                # Add a list of commands for the client to see and not be printed to console
                Write.Print(Help.menu, Colors.white_to_black, interval=0.01)
            else:
                self.send(to_send)

    def run(self):
        self.connect()

        receive_thread = threading.Thread(target=self.receive)
        input_thread = threading.Thread(target=self.input_thread)

        receive_thread.start()
        input_thread.start()

        receive_thread.join()
        input_thread.join()

if __name__ == '__main__':
    client = Client()
    try: client.run()
    except KeyboardInterrupt: print("\nConnection ended!"); exit(0)
