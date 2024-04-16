import html
import os

from src.repository.sharepoint import Sharepoint


class PagesGenerator:
    _template_aspx_path = "assets", "template", "template.aspx"
    _common_assets_path = "assets", "common"

    def __init__(self):
        self.common_assets = self._load_common_assets()
        self.pages = {}

        template_aspx_path = os.path.join(*self._template_aspx_path)
        self._template_aspx = self._read(template_aspx_path)

        self.sharepoint_repository = Sharepoint()

    @staticmethod
    def _read(path: str) -> str:
        with open(path, 'rb') as file:
            return file.read().decode('utf-8')

    def _load_common_assets(self) -> dict:
        common_assets_path = os.path.join(*self._common_assets_path)
        files = os.listdir(common_assets_path)
        common_assets = {}
        for file_name in files:
            file_id = ".".join(file_name.split(".")[:-1])
            file_path = os.path.join(common_assets_path, file_name)
            common_assets[file_id] = self._read(file_path)
        return common_assets

    def _generate_page_aspx(self, title: str, content: str, ) -> bytes:
        content = html.escape(content)
        page_aspx = (
            self._template_aspx
            .replace("{page_content}", content)
            .replace("{page_title}", title)
        )
        page_aspx_bytes = page_aspx.encode()
        return page_aspx_bytes

    def generate_pages(self):
        for page_path, page_content in self.pages.items():
            page_title = page_path.split("/")[-1]
            page_aspx = self._generate_page_aspx(page_title, page_content)
            self.sharepoint_repository.upload_page(f"{page_path}.aspx", page_aspx)
