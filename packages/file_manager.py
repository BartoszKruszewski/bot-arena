import os

folders = ['BOTS', 'LOGS', 'MAPS']

class FileManagerException(Exception):
    pass

class FileManager():
    def __init__(self, name):
        if name not in folders:
            raise FileManagerException(f'Folder {name} not allowed')
        self.name = name
        self.path = os.path.join(os.getcwd(), name)

    def create_file(self, file_name, text=""):
        file_path = os.path.join(self.path, file_name)

        if text == "":
            raise FileManagerException('Creation of empty files is not allowed')
        if "example" in file_name:
            raise FileManagerException('Creation of example files is not allowed')
        
        with open(file_path, 'w') as file:
            file.write(text)

    def read_file(self, file_name) -> str:
        file_path = os.path.join(self.path, file_name)

        if not os.path.exists(file_path):
            raise FileManagerException(f'File {file_name} not found')
        
        with open(file_path, 'r') as file:
            return file.read()
        
    def delete_file(self, file_name):
        file_path = os.path.join(self.path, file_name)
        if "example" in file_name:
            raise FileManagerException('Deletion of example files is not allowed')
        os.remove(file_path)

    def get_files(self) -> list:
        return os.listdir(self.path)
    

MAP_MANAGER = FileManager('MAPS')
BOT_MANAGER = FileManager('BOTS')
LOG_MANAGER = FileManager('LOGS')