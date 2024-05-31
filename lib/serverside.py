"""
    This file is to create, handle and manage the serverside functions
    available to be executed. It also allows `fuzz.py` to be able to use these
    in it's fuzzy search.
"""

import os
import sys
import subprocess

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from server import Server

class Serverside:
    def __init__(self) -> None:
        ...
    
    def run(self, command: str, args: str = None, output: bool = True) -> bytes:
        return subprocess.run([command, args], capture_output=output)

    # each function to do it's own thing UNLESS it's needed within the client's side

    def server_off(self) -> None:
        """Close all connections to the server!"""
        self.server.close()


if __name__ == '__main__':
    ss = Serverside()
    print(
        ss.run("ls", "-l", False)
    )