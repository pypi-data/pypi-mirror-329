import os
import shutil

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