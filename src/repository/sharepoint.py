import requests
from decouple import config
from datetime import datetime
from src.repository.sharepoint_auth import SharepointAuth


class SharepointDocuments:
    def __init__(
            self,
            site_url=config("site_url"),
            client_id=config("client_id"),
            client_secret=config("client_secret"),
            cache_json_file_name="cache/sharepoint_auth.json",
    ):
        """
        :param site_url:
        :param client_id:
        :param client_secret:
        :param cache_json_file_name: If no cache file is wanted, provide an empty value for this var
        """

        self.site_url = site_url
        self.auth = SharepointAuth(
            site_url=site_url,
            client_id=client_id,
            client_secret=client_secret,
            cache_json_file_name=cache_json_file_name,
        )
        self.access_token = None
        self.access_token_expiration = 0

    def list_documents(self, folder: str) -> str:
        access_token = self._get_token()
        headers = {"Authorization": "Bearer " + access_token}
        url = f"{self.site_url}/_api/web/GetFolderByServerRelativeUrl('{folder}')"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text

    def upload_file(self, file_path: str, content: bytes, folder: str) -> str:
        access_token = self._get_token()
        headers = {"Authorization": "Bearer " + access_token}
        url = f"{self.site_url}/_api/web/GetFolderByServerRelativeUrl('{folder}')/Files/add(url='{file_path}',overwrite=true)"
        response = requests.post(url, headers=headers, data=content)
        response.raise_for_status()
        return response.text

    def download_file(self, folder: str, file: str) -> bytes:
        access_token = self._get_token()
        headers = {"Authorization": "Bearer " + access_token}
        url = f"{self.site_url}/_api/web/GetFolderByServerRelativeUrl('{folder}')/Files('{file}')/$value"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.content

    def _get_token(self) -> str:
        time_now = datetime.now().timestamp()
        if time_now > self.access_token_expiration:
            token, valid_until = self.auth.get_token(time_now)
            self.access_token_expiration = valid_until
            self.access_token = token
        return self.access_token
