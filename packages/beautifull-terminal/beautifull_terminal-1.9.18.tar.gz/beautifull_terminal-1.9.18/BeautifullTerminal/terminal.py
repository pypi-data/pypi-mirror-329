import builtins

class BeautifullTerminal:
    COLORS = {
        "reset": "\033[0m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "green": "\033[92m",
        "white": "\033[97m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "black": "\033[90m",
        "light_red": "\033[91m",
        "light_green": "\033[92m",
        "light_yellow": "\033[93m",
        "light_blue": "\033[94m",
        "light_cyan": "\033[96m",
        "light_magenta": "\033[95m",
        "dark_gray": "\033[90m",
        "light_gray": "\033[37m",
        "orange": "\033[38;5;208m",
        "purple": "\033[38;5;128m",
        "teal": "\033[38;5;38m",
        "pink": "\033[38;5;206m",
        "brown": "\033[38;5;94m",
        "gold": "\033[38;5;226m",
        "navy": "\033[38;5;17m",
        "dark_green": "\033[38;5;22m",
    }

    def __init__(self):
        self.original_print = builtins.print
        self.enable()

    def enable(self):
        builtins.print = self.custom_print

    def disable(self):
        builtins.print = self.original_print

    def custom_print(self, *args, color=None, **kwargs):
        message = " ".join(map(str, args))

        if color and color.lower() in self.COLORS:
            color = self.COLORS[color.lower()]
        elif "error" in message.lower():
            color = self.COLORS['red']
        elif "warn" in message.lower():
            color = self.COLORS['yellow']
        elif "success" in message.lower():
            color = self.COLORS['green']
        else:
            color = self.COLORS['reset']

        self.original_print(f"{color}{message}{self.COLORS['reset']}", **kwargs)