import requests
from ..transport.sharepoint_auth import SharepointAuthApi


class SharepointDocumentsApi:
    def __init__(
            self,
            site_url: str,
            client_id: str,
            client_secret: str,
            tenant_id: str = None,
            cache_json_file_path: str = None,
            proxies: dict = None
    ):
        """
        :param site_url:
        :param client_id:
        :param client_secret:
        :param tenant_id: *Optional*
        :param cache_json_file_path: *Optional* If given, the values will be cached in a local json file.
        :param proxies: *Optional* Https proxies.
        """
        self.proxies = proxies or {}
        self.site_url = site_url
        self.auth = SharepointAuthApi(
            site_url=site_url,
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id,
            cache_json_file_path=cache_json_file_path,
            proxies=self.proxies,
        )

    def list_documents(self, folder: str = "Shared Documents") -> str:
        access_token = self.auth.get_token()
        headers = {"Authorization": "Bearer " + access_token}
        url = f"{self.site_url}/_api/web/GetFolderByServerRelativeUrl('{folder}')"
        response = requests.get(url, headers=headers, proxies=self.proxies)
        response.raise_for_status()
        return response.text

    def create_folder(self, folder: str) -> bool:
        access_token = self.auth.get_token()
        headers = {"Authorization": "Bearer " + access_token}
        folders = folder.split("/")
        active_folder = folders.pop(0)
        for folder in folders:
            active_folder += "/"+folder
            url = f"{self.site_url}/_api/web/Folders/add(url='{active_folder}')"
            response = requests.post(url, headers=headers, proxies=self.proxies)
            response.raise_for_status()
        return True

    @staticmethod
    def _separate_file_name_and_folder(file_path: str, main_folder: str) -> tuple:
        file_path = file_path.replace("\\", "/")
        main_folder = main_folder.replace("\\", "/")

        file_path = file_path[::-1].split("/", 1)
        if len(file_path) > 1:
            file_name, file_folders = file_path[0][::-1], file_path[1][::-1]
            main_folder += "/" + file_folders
        else:
            file_name = file_path[0][::-1]
        return file_name, main_folder.replace("//", "/")

    def upload_file_by_path(self, file_name: str, file_path: str, main_folder: str = "Shared Documents") -> str:
        with open(file_path, "rb") as file:
            file_content = file.read()
        self.upload_file(file_name, file_content, main_folder)

    def upload_file(self, file_name: str, content: bytes, main_folder: str = "Shared Documents") -> str:
        access_token = self.auth.get_token()
        headers = {"Authorization": "Bearer " + access_token}
        file_name, folder = self._separate_file_name_and_folder(file_name, main_folder)

        url = f"{self.site_url}/_api/web/GetFolderByServerRelativeUrl('{folder}')/Files/add(url='{file_name}',overwrite=true)"
        response = requests.post(url, headers=headers, proxies=self.proxies, data=content)
        if response.status_code == 404:
            self.create_folder(folder)
            response = requests.post(url, headers=headers, proxies=self.proxies, data=content)
        response.raise_for_status()
        return response.text

    def download_file(self, file: str, folder: str = "Shared Documents") -> bytes:
        access_token = self.auth.get_token()
        headers = {"Authorization": "Bearer " + access_token}
        url = f"{self.site_url}/_api/web/GetFolderByServerRelativeUrl('{folder}')/Files('{file}')/$value"
        response = requests.get(url, headers=headers, proxies=self.proxies)
        response.raise_for_status()
        return response.content
