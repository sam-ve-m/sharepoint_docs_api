import json
from datetime import datetime

import requests
from ..repository.mini_db import MiniDB


class SharepointAuthApi:
    def __init__(self, site_url: str, client_id: str, client_secret: str, tenant_id: str, cache_json_file_path: str, proxies: dict):
        self.site_url = site_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.proxies = proxies

        if cache_json_file_path:
            self.database = MiniDB(cache_json_file_path, site_url)
        else:
            self._search_tenant_id = self._fetch_tenant_id
            self._search_token = self._generate_token

        self.token = None
        self.valid_until = 0

    def _fetch_tenant_id(self) -> str:
        url = f"{self.site_url}/_vti_bin/client.svc/"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, proxies=self.proxies)
        report_to = json.loads(response.headers.get('Report-To', '{}'))
        endpoint = report_to.get('endpoints', [{}])[0]
        tenant_id_param = next(param.split("=")[1] for param in endpoint.get('url', '').split("?")[1].split("&") if
                               param.startswith("tenantId"))
        return tenant_id_param

    def _get_tenant_id(self):
        if not self.tenant_id:
            self.tenant_id = self._search_tenant_id()
        return self.tenant_id

    def _search_tenant_id(self):
        if not (tenant_id := self.database.get('tenant_id')):
            tenant_id = self._fetch_tenant_id()
            self.database.set('tenant_id', tenant_id)
        return tenant_id

    def _generate_token(self, time_now: float) -> tuple:
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
        response = requests.post(url, headers=headers, proxies=self.proxies, data=data)
        response.raise_for_status()
        response_json = response.json()
        token, valid_until = response_json.get('access_token'), float(response_json.get('expires_on'))
        assert time_now < valid_until, "An expired token was given"
        return token, valid_until

    def _search_token(self, time_now: float) -> tuple:
        if time_now > self.database.get('access_token_expiration', 0):
            token, valid_until = self._generate_token(time_now)
            self.database.set('access_token_expiration', valid_until)
            self.database.set('access_token', token)
        else:
            token = self.database.get('access_token')
            valid_until = self.database.get('access_token_expiration')
        return token, valid_until

    def get_token(self) -> str:
        time_now = datetime.now().timestamp()
        if time_now > self.valid_until:
            self.token, self.valid_until = self._search_token(time_now)
        return self.token
