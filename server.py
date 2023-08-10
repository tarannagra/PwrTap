import socket
import tomllib
import subprocess


class Server:
    def __init__(self) -> None:
        self.data = tomllib.load(open('conf.toml', 'rb'))

        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.host = self.data["server"]["host"]
        self.port = self.data["server"]["port"]
    
    def init(self, max_connections:int=10):
        try:
            self.server.bind((
                self.host,
                self.port,
            ))
            print(f"Successfully bound to {self.host}:{self.port}")
        except socket.error as error:
            print(f"[E] {error}")
            exit(1)
        finally:
            self.server.listen(max_connections)
            print(f"Server listening on port {self.port}.\nAwaiting data...")
    
    def parse(self, content:str) -> None:
        match content:
            case "clear screen":
                subprocess.run(['clear'])
            case "stop server":
                exit(0)

    def start(self, buffer:int=4096):
        while True:
            try:
                client_sock, client_addr = self.server.accept()
                print(f"{client_addr[0]}:{client_addr[1]} connected to the server!")
                
                while True:
                    self.data = client_sock.recv(buffer).decode()
                    if not self.data:
                        print(f"{client_addr[0]}:{client_addr[1]} disconnected from the server!")
                        break
                    self.parse(self.data)
                    print(f"Received from: {client_addr[0]}:{client_addr[1]}: {self.data}")
                client_sock.close()
            except ConnectionResetError:
                print("User has disconnected!")

if __name__ == '__main__':
    server = Server()
    server.init()
    server.start()