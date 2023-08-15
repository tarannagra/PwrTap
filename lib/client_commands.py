# Built in modules
import subprocess

# External modules
from pystyle import (
    Write,
    Colors,
)

# Local modules
from lib.design import Help

class Commands:
    def __init__(self) -> None:
        # 1 command
        self.run = lambda x: subprocess.run([x])
        
    
    # Clear client-side screen
    def clear(self) -> None:
        self.run("clear")
    
    # Display menus
    def help_menu(self) -> None:
        Write.Print(
            Help.menu,
            Colors.dark_red,
            interval=0.01
        )

    # Git commands

    

if __name__ == '__main__':
    commands = Commands()
    print(commands.clear())