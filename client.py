
# Built in modules
import subprocess
import socket
import threading
import tomllib

# External modules
from colorama import Fore, init;init(autoreset=True)

# Local modules
from lib.clientside import Commands

commands = Commands()

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
            print(f"Trying to connect to {self.host}:{self.port}...")
            self.client.connect((self.host, self.port))
        except socket.error:
            print(f"Connection timeout...")
            exit(1)
        print(f"Connected to {self.host}:{self.port}")
        
    def send(self, content: str) -> None:
        content = content.encode()
        self.client.send(content)

    def receive(self):
        while True:
            try:
                data = self.client.recv(4096)
                if not data:
                    self.client.detach()
                    break
            except (OSError, EOFError):
                print(f"Disconnected from {self.host}:{self.port}")
                break
        self.client.close()

    def input_thread(self):
        while True:
            try:
                to_send = input("> ")
                match to_send:
                    case "help" | "?":
                        commands.help_menu()
                    case "clear screen" | "clear":
                        commands.clear()
                    case _:
                        self.send(to_send)
            except (ConnectionRefusedError, OSError, EOFError):
                print(f"{Fore.RED}Server has been turned off!")
                exit(0)

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
