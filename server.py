
import re
import time
import socket
import tomllib
import subprocess

# External modules
from colorama import Fore, init; init(autoreset=True)

# fuzzy
import nltk
import numpy as np
from thefuzz import fuzz
from nltk.chat.util import Chat, reflections
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

# local imports
# from lib.serverside import Serverside

class Server:
    def __init__(self, shutdown_delay: int = 60) -> None:
        nltk.download("punkt")
        self.shutdown_delay = shutdown_delay
        self.data = tomllib.load(open('conf.toml', 'rb'))

        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.host = self.data["server"]["host"]
        self.port = self.data["server"]["port"]
   
        # fuzzy logic responses
        self.responses = [
            ["restart the computer", ["...restarting..."]],
            ["turn off the computer", ["...computer turning off..."]],
            ["open this app on the computer", ["...opening app..."]],
            ["log off the computer", ["...opening app..."]],
            ["turn the volume up", ["...volume up..."]],
        ]

    
    # fuzzy logic methods
    def starter(self) -> None:
        Chat(
            pairs=self.responses,
            reflections=reflections
        )
        self.start()
    
    def get_fuzzy_score(self, _input: str, pattern: str) -> int:
        """Check the message and match it to the most appropriate response and return the score"""
        return fuzz.partial_ratio(_input.lower(), pattern.lower())
    
    def train_model(self, data: list[str], labels: list[str]) -> tuple[TfidfVectorizer, MultinomialNB]:
        """Train the model with the given data and labels. Return the vectorizer and model."""
        vect = TfidfVectorizer()
        feats = vect.fit_transform(data)
        model = MultinomialNB()
        model.fit(feats, labels)
        return vect, model

    def predict(self, _input: str, vectorizer: TfidfVectorizer, model: MultinomialNB) -> int:
        """Predict the response based on the score."""
        vectored_input = vectorizer.transform([_input])
        pred = model.predict(vectored_input)
        return pred[0]

    def init(self, max_connections:int=10):
        try:
            self.server.bind((
                self.host,
                self.port,
            ))
            print(f"{Fore.GREEN}Successfully bound to {self.host}:{self.port}")
        except socket.error as error:
            print(f"[E] {error}")
            exit(1)
        finally:
            self.server.listen(max_connections)
            print(f"{Fore.GREEN}Server listening on port {self.port}.\nAwaiting data...")
    
    def parse(self, content:str, vector, model) -> None:
        f_scores = [self.get_fuzzy_score(content, pattern) for pattern, _ in self.responses]
        max_score = np.argmax(f_scores)
        f_response = self.responses[max_score][1][0]

        ml_intent = self.predict(content, vector, model)
        ml_response = self.responses[ml_intent][1][0]

        response = f_response if max(f_scores) >= 70 else ml_response
        return response


    def start(self, buffer:int=4096):
        self.init()
        data = [response[0] for response in self.responses]
        labels = range(len(self.responses))

        try:
            vector, model = self.train_model(data, labels)
            c_sock, c_addr = self.server.accept()
            print(f"{Fore.GREEN}{c_addr[0]}:{c_addr[1]} has connected.")         
            while True:
                self.data = c_sock.recv(buffer).decode()
                if not self.data:
                    print(f"{Fore.YELLOW}{c_addr[0]}:{c_addr[1]} has disconnected!")
                    break
                if fuzz.partial_ratio(self.data.lower(), "turn off the server") >= 70:
                    print(f"{Fore.YELLOW}Received server shutdown request. Shutting down in 3 seconds...")
                    time.sleep(3)
                    self.server.close()
                    exit(0)
                elif fuzz.partial_ratio(self.data.lower(), "open this {app} on the computer") >= 70:
                    pattern = r"open (.+?)(?: on the computer)?$"
                    print(f"Opening: {re.search(pattern, self.data.lower()).group(1)}")
                elif fuzz.partial_ratio(self.data.lower(), "turn the computer off") >= 70:
                    print(f"{Fore.YELLOW}Received server shutdown request. Shutting down in 60 seconds...\nTo stop this on the server, type in: 'shutdown -a'")
                    subprocess.run(["shutdown", "-s", "-t", self.shutdown_delay])
                    
                else:
                    f_scores = [self.get_fuzzy_score(self.data, pattern) for pattern, _ in self.responses]
                    max_score = np.argmax(f_scores)
                    f_resp = self.responses[max_score][1][0]

                    ml_intent = self.predict(self.data, vector, model)
                    ml_resp = self.responses[ml_intent][1][0]

                    response = f_resp if max(f_scores) >= 70 else ml_resp

                    print(f"{Fore.YELLOW}> {Fore.LIGHTWHITE_EX}{response}")
               

        except ConnectionResetError:
            print(f"{Fore.RED}A user has been disconnected!")


if __name__ == '__main__':
    server = Server()
    server.starter()