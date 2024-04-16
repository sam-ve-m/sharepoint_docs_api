import os

from src.service.generator.pages_generator import PagesGenerator


class ImeaPagesGenerator(PagesGenerator):
    _pages_path = "assets", "pages"

    def _default_generation(self, page_name: str, *page_path):
        page_path = os.path.join(*self._pages_path, *page_path)
        page = self._read(page_path)
        page = page.split("{{")
        page_parts = [page[0]]

        if len(page) != 1:
            for part in page[1:]:
                common_asset_id, content = part.split("}}")
                common_asset = self.common_assets[common_asset_id.rstrip().strip()]
                page_parts.append(common_asset)
                page_parts.append(content)

        page = "".join(page_parts)
        self.pages[page_name] = page
        return self

    def generate_relatorio(self):
        return self._default_generation("RelatoriosDeMercado", "relatorio", "main.html")

    def generate_relatorios(self):
        ...
        return self


