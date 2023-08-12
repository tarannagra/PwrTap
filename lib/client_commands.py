import subprocess

class Commands:
    def __init__(self) -> None:
        # 1 command
        self.run = lambda x: subprocess.run([x])
    
    # Git commands

    """
    TODO:
        Move all client commands here and when they are needed,
        just call the command like `Commands.x()` or `commands = Commands(); commands.x()`
    """