import multiprocessing
import os

from sharepoint_api_transport import SharepointDocumentsApi


class DumpFolder:
    def __init__(self, folder: str = "../temp"):
        self.folder = folder
        self.files = []
        self.search_file()
        self.sharepoint = SharepointDocumentsApi(

        )

    def search_file(self):
        for root, directories, files in os.walk(self.folder):
            for filename in files:
                file_path = os.path.join(root, filename)
                self.files.append(file_path)

    def upload_file(self, file_path: str):
        file_name = file_path.replace(self.folder, "")
        self.sharepoint.upload_file_by_path(file_name, file_path)

    def upload_files(self):
        self.upload_file(self.files[0])
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            pool.map(self.upload_file, self.files)

