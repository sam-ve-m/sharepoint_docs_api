import multiprocessing
import os

from lib import SharepointDocuments


class DumpFolder:
    def __init__(self, folder: str = "../temp"):
        self.folder = folder
        self.files = []
        self.search_file()
        self.sharepoint = SharepointDocuments()

    def search_file(self):
        for root, directories, files in os.walk(self.folder):
            for filename in files:
                file_path = os.path.join(root, filename)
                self.files.append(file_path)

    def upload_file(self, file_path: str):
        file_name = file_path.replace(self.folder, "")
        if file_name[0] in ("\\", "/"):
            file_name = file_name[1:]
        with open(file_path, "wb") as file:
            file_content = file.read()
        self.sharepoint.upload_file(file_name, file_content)

    def upload_files(self):
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            pool.map(self.upload_file, self.files)

