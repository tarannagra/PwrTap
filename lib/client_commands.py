# Built in modules
import subprocess

# External modules
from pystyle import (
    Write,
    Colors,
)

# Local modules
import lib.design

class Commands:
    def __init__(self) -> None:
        # 1 command
        self.run = lambda x: subprocess.run([x])
        self.help = lib.design.Help
        self.help_menu = self.help.menu
    
    # Clear client-side screen
    def clear(self) -> None:
        self.run("clear")
    
    # Display menus
    def help_menu(self) -> None:
        Write.Print(
            self.help_menu,
            Colors.dark_red,
            interval=0.01
        )

    # Git commands

    

if __name__ == '__main__':
    commands = Commands()
    print(commands.clear())