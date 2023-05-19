import os


class ProjectManager:
    def __init__(self, directory):
        self.directory = directory

    def create_project_dir(self):
        """Create a directory for the project if it doesn't exist."""
        if not os.path.exists(self.directory):
            print(f"Creating directory {self.directory}")
            os.makedirs(self.directory)
