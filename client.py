import socket
import threading
import tomllib

class Client:
    def __init__(self) -> None:
        self.data = tomllib.load(open('conf.toml', 'rb'))

        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
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
                break
            print(f"Received: {data.decode()}")

    def input_thread(self):
        while True:
            to_send = input("> ")
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
    except KeyboardInterrupt: print("Connection ended!"); exit(0)
