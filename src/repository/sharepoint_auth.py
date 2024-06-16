import json
import requests
from src.repository.mini_db import MiniDB


class SharepointAuth:
    def __init__(self, site_url: str, client_id: str, client_secret: str, cache_json_file_name: str):
        self.site_url = site_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.database = MiniDB(cache_json_file_name)

        self.tenant_id = None

    def _fetch_tenant_id(self) -> str:
        url = f"{self.site_url}/_vti_bin/client.svc/"
        headers = {
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)",
        }
        response = requests.get(url, headers=headers)
        report_to = json.loads(response.headers.get('Report-To'))
        tenant_id = tuple(filter(lambda x: "tenant" in x, report_to.get('endpoints')[0].get('url').split("?")[1].split("&")))[0].split("=")[1]
        assert tenant_id, "Missing tenant id"
        return tenant_id

    def _get_tenant_id(self):
        if not self.tenant_id:
            self.tenant_id = self._search_tenant_id()
        return self.tenant_id

    def _search_tenant_id(self):
        if not (tenant_id := self.database.get('tenant_id')):
            tenant_id = self._fetch_tenant_id()
            self.database.set('tenant_id', tenant_id)
        return tenant_id

    def _generate_token(self) -> tuple:
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
        response.raise_for_status()
        response_json = response.json()
        return response_json.get('access_token'), float(response_json.get('expires_on'))

    def get_token(self, time_now: float) -> tuple:
        if time_now > self.database.get('access_token_expiration', 0):
            token, valid_until = self._generate_token()
            self.database.set('access_token_expiration', valid_until)
            self.database.set('access_token', token)
        else:
            token = self.database.get('access_token')
            valid_until = self.database.get('access_token_expiration')
        return token, valid_until
