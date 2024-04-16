import json
import requests
from decouple import config
from src.repository.mini_db import MiniDB


class Sharepoint:
    def __init__(self):
        self.site_url = config("site_url")
        self.client_id = config("client_id")
        self.client_secret = config("client_secret")
        self.database = MiniDB("database.json")

    def list_documents(self, folder: str) -> str:
        access_token = self._get_token()
        headers = {"Authorization": "Bearer " + access_token}
        url = f"{self.site_url}/_api/web/GetFolderByServerRelativeUrl('{folder}')"
        response = requests.get(url, headers=headers)
        return response.text

    def upload_page(self, file_path: str, content: bytes, folder: str = "Pages") -> str:
        access_token = self._get_token()
        headers = {"Authorization": "Bearer " + access_token}
        url = f"{self.site_url}/_api/web/GetFolderByServerRelativeUrl('{folder}')/Files/add(url='{file_path}',overwrite=true)"
        response = requests.post(url, headers=headers, data=content)
        return response.text

    def _fetch_tenant_id(self) -> str:
        url = f"{self.site_url}/_vti_bin/client.svc/"
        headers = {
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)",
        }
        response = requests.get(url, headers=headers)
        report_to = json.loads(response.headers.get('Report-To'))
        tenant_id = tuple(filter(lambda x: "tenant" in x, report_to.get('endpoints')[0].get('url').split("?")[1].split("&")))[0].split("=")[1]
        return tenant_id

    def _get_tenant_id(self):
        if not (tenant_id := self.database.get('tenant_id')):
            tenant_id = self._fetch_tenant_id()
            self.database.set('tenant_id', tenant_id)
        return tenant_id

    def _generate_token(self) -> str:
        tenant_id = self._get_tenant_id()
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        clean_site_url = self.site_url.replace('https://', '').split('/')[0]
        resource = f"00000003-0000-0ff1-ce00-000000000000/{clean_site_url}@{tenant_id}"
        data = {
            "client_id": self.client_id + "@" + tenant_id,
            "resource": resource,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        url = f"https://accounts.accesscontrol.windows.net/{tenant_id}/tokens/OAuth/2"
        response = requests.post(url, headers=headers, data=data)
        response_json = response.json()
        return response_json.get('access_token')

    def _get_token(self) -> str:
        if not (token := self.database.get('access_token')):
            token = self._generate_token()
            self.database.set('access_token', token)
        return token
