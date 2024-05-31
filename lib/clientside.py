# Built in modules
import subprocess
from typing import (
    Union,
)

# External modules
from pystyle import (
    Write,
    Colors,
)

# Local modules
from lib.design import Help

class Commands:
    def __init__(self) -> None:
        self.run = lambda x: subprocess.run(x)
        
    
    # Clear client-side screen
    def clear(self) -> None:
        self.run(["clear"])
    
    # Display menus
    def help_menu(self) -> None:
        Write.Print(
            Help.menu,
            Colors.dark_red,
            interval=0.01
        )

    # Git commands
    # I find it easier to implement adding and pushing into programs I make
    def git_add(self, file="."):
        self.run(["git", "add", file])

    

if __name__ == '__main__':
    commands = Commands()
    print(commands.clear())