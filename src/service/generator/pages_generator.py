import html
import os

from src.repository.sharepoint import Sharepoint


class PagesGenerator:
    _template_aspx_path = "assets", "template", "template.aspx"
    _common_assets_path = "assets", "common"
    common_assets = {}
    pages = {}

    def __init__(self):
        self._load_common_assets_folder(os.path.join(*self._common_assets_path))
        template_aspx_path = os.path.join(*self._template_aspx_path)
        self._template_aspx = self._read(template_aspx_path)
        self.sharepoint_repository = Sharepoint()

    @staticmethod
    def _read(path: str) -> str:
        with open(path, 'rb') as file:
            return file.read().decode('utf-8')

    @staticmethod
    def _save(path: str, file_content: str):
        with open(path, 'w') as file:
            return file.write(file_content)

    def _load_common_asset(self, path: str, file_name: str):
        file_id = ".".join(file_name.split(".")[:-1])
        self.common_assets[file_id] = self._read(path)

    def _load_common_assets_folder(self, path: str, name_prefix: str = ""):
        items = os.listdir(path)
        for item in items:
            item_path = os.path.join(path, item)
            item_name = name_prefix + item
            if os.path.isdir(item_path):
                self._load_common_assets_folder(item_path, item_name + ".")
            else:
                self._load_common_asset(item_path, item_name)

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
        for page_full_path, page_content in self.pages.items():
            page_name = page_full_path.split("/")[-1]
            page_folder = page_full_path.replace(page_name, "")[:-1]
            page_aspx = self._generate_page_aspx(page_name, page_content)
            self.sharepoint_repository.upload_page(f"{page_name}.aspx", page_aspx, page_folder)
