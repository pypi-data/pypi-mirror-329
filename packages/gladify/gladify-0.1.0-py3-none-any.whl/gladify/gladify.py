import os
import shutil

class Gmath:
    def __init__(self):
        self.result = None
    
    def out(self, string=""):
        print(f"{string}{self.result}")
        return self
    
    def power(self, number, to):
        self.result = number ** to
        return self

    def rnd(self, number):
        self.result = round(number)
        return self
        
    def numroot(self, number, power):
        self.result = number ** (1/power)
        return self

    def PoL(self, invest, back, currency="$"):
        currency = str(currency)

        if (currency.isdigit()):
            raise ValueError("The currency cannot be a number.")

        if (len(currency) != 1):
            raise ValueError("The currency can only be up to 1 character and must be greater than 0.")

        if (invest == back):
            self.result = "NO PROFIT OR LOSS"
        elif (invest < back):
            money = back - invest
            self.result = f"PROFIT of {currency}{money}"
        else:
            money = invest - back
            self.result = f"LOSS of {currency}{money}"
        return self

    def area2(self, shape, x=0, y=0):
        shapes = ["circle", "square", "rectangle", "triangle", "parallelogram", "rhombus", "ellipse"]
        shape = shape.lower()
        if (shape not in shapes):
            raise ValueError(f"Invalid 2D shape '{shape}'.")
        else:
            if (shape == "circle"):
                self.result = 3.14159 * x ** 2
            elif (shape == "square"):
                self.result = x * x
            elif (shape == "rectangle"):
                self.result = x * y
            elif (shape == "triangle"):
                self.result = 1/2 * x * y
            elif (shape == "parallelogram"):
                self.result = x * y
            elif (shape == "rhombus"):
                self.result = 1/2 * x * y
            elif (shape == "ellipse"):
                self.result = 3.14159 * x * y
        return self

    def tsa3(self, shape, x=0, y=0, z=0):
        shape = shape.lower()
        shapes = ["cube", "cuboid", "cylinder", "sphere", "cone", "hemisphere"]
        if (shape not in shapes):
            raise ValueError(f"Invalid 3D shape '{shape}'.")
        else:
            if (shape == "cube"):
                self.result = 6 * x ** 2
            elif (shape == "cuboid"):
                self.result = 2 * (x * y + x * z + y * z)
            elif (shape == "sphere"):
                self.result = 4 * 3.14159 * x ** 2
            elif (shape == "cylinder"):
                self.result = 2 * 3.14159 * x * (x + y)
            elif (shape == "cone"):
                self.result = 3.14159 * x * (x + y)
            elif (shape == "hemisphere"):
                self.result = 3 * 3.14159 * x ** 2
        return self

    def perimeter2(self, shape, x=0, y=0):
        shapes = ["circle", "square", "rectangle", "triangle"]
        shape = shape.lower()
        if (shape not in shapes):
            raise ValueError(f"Invalid 2D shape '{shape}'.")
        else:
            if (shape == "circle"):
                self.result = 2 * 3.14159 * x
            elif (shape == "square"):
                self.result = 4 * x
            elif (shape == "rectangle"):
                self.result = 2 * (x + y)
            elif (shape == "triangle"):
                self.result = x + y + ((x**2 + y**2) ** 0.5)  # Assuming right triangle
        return self

    def vol3(self, shape, x=0, y=0, z=0):
        shapes = ["cube", "cuboid", "cylinder", "sphere", "cone", "hemisphere"]
        shape = shape.lower()
        if (shape not in shapes):
            raise ValueError(f"Invalid 3D shape '{shape}'.")
        else:
            if (shape == "cube"):
                self.result = x ** 3
            elif (shape == "cuboid"):
                self.result = x * y * z
            elif (shape == "sphere"):
                self.result = (4 / 3) * 3.14159 * x ** 3
            elif (shape == "cylinder"):
                self.result = 3.14159 * x ** 2 * y
            elif (shape == "cone"):
                self.result = (1 / 3) * 3.14159 * x ** 2 * y
            elif (shape == "hemisphere"):
                self.result = (2 / 3) * 3.14159 * x ** 3
        return self

class Gtext:
    fg_code = {
        "black": "\033[30m", "red": "\033[31m", "green": "\033[32m", "yellow": "\033[33m",
        "blue": "\033[34m", "magenta": "\033[35m", "cyan": "\033[36m", "white": "\033[37m",
        "gray": "\033[90m", "light_red": "\033[91m", "light_green": "\033[92m", "light_yellow": "\033[93m",
        "light_blue": "\033[94m", "light_magenta": "\033[95m", "light_cyan": "\033[96m", "light_white": "\033[97m"
    }

    bg_code = {
        "black": "\033[40m", "red": "\033[41m", "green": "\033[42m", "yellow": "\033[43m",
        "blue": "\033[44m", "magenta": "\033[45m", "cyan": "\033[46m", "white": "\033[47m",
        "gray": "\033[100m", "light_red": "\033[101m", "light_green": "\033[102m", "light_yellow": "\033[103m",
        "light_blue": "\033[104m", "light_magenta": "\033[105m", "light_cyan": "\033[106m", "light_white": "\033[107m"
    }

    format_code = {
        "bold": "\033[1m", "dim": "\033[2m", "italic": "\033[3m", "underline": "\033[4m",
        "blink": "\033[5m", "reverse": "\033[7m", "hidden": "\033[8m"
    }

    def __init__(self):
        self.result = None

    def out(self, string=""):
        print(f"{string}{self.result}")
        return self

    def outStyle(self, text, fg=None, bg=None, design=None):
        style = []

        if fg:
            fg = fg.lower()
            if fg in self.fg_code:
                style.append(self.fg_code[fg])
            else:
                raise ValueError(f"Invalid foreground color '{fg}'.")

        if bg:
            bg = bg.lower()
            if bg in self.bg_code:
                style.append(self.bg_code[bg])
            else:
                raise ValueError(f"Invalid background color '{bg}'.")

        if design:
            if not isinstance(design, tuple):  # Ensure design is a tuple
                raise ValueError("Design must be a tuple, e.g., ('bold', 'italic').")
            for d in design:
                d = d.lower()
                if d in self.format_code:
                    style.append(self.format_code[d])
                elif d in ["b", "u"]:  # Allow 'b' for bold and 'u' for underline
                    style.append(self.format_code["bold"] if d == "b" else self.format_code["underline"])
                else:
                    raise ValueError(f"Invalid text format '{d}'.")

        self.result = f"{''.join(style)}{text}\033[0m"
        return self

class Gfile:
    def __init__(self, path=None):
    	self.path = path or os.getcwd()  # Default to current directory

    def selected_path(self, new_path):
    	"""Change the working directory, creating it if necessary."""
    	self.path = new_path
    	os.makedirs(new_path, exist_ok=True)  # Ensure the directory exists

    def list_items(self):
        """List all files and folders in the current directory."""
        return os.listdir(self.path)

    def create_file(self, filename, content=""):
        """Create a file with optional content."""
        with open(os.path.join(self.path, filename), "w") as file:
            file.write(content)

    def read_file(self, filename):
        """Read the content of a file."""
        with open(os.path.join(self.path, filename), "r") as file:
            return file.read()

    def append_file(self, filename, content):
        """Append text to an existing file."""
        with open(os.path.join(self.path, filename), "a") as file:
            file.write(content)

    def delete_file(self, filename):
        """Delete a file."""
        os.remove(os.path.join(self.path, filename))

    def create_folder(self, foldername):
        """Create a new folder."""
        os.makedirs(os.path.join(self.path, foldername), exist_ok=True)

    def delete_folder(self, foldername):
        """Delete a folder and its contents."""
        shutil.rmtree(os.path.join(self.path, foldername))

    def move(self, source, destination):
        """Move or rename a file/folder."""
        shutil.move(os.path.join(self.path, source), os.path.join(self.path, destination))

    def copy(self, source, destination):
        """Copy a file or folder."""
        full_src = os.path.join(self.path, source)
        full_dest = os.path.join(self.path, destination)

        if os.path.isdir(full_src):
            shutil.copytree(full_src, full_dest)
        else:
            shutil.copy2(full_src, full_dest)

    def file_info(self, filename):
        """Get file size and modification time."""
        full_path = os.path.join(self.path, filename)
        return {
            "size": os.path.getsize(full_path),
            "modified": os.path.getmtime(full_path),
        }

    def exists(self, name):
        """Check if a file or folder exists."""
        return os.path.exists(os.path.join(self.path, name))

    def path_info(self):
        """Get the current working directory."""
        return self.path