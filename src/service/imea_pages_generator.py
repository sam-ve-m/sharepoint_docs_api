import os

from src.service.generator.pages_generator import PagesGenerator


def remove_diacritics(input_str):
    mapping = {
        'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c',
        'ñ': 'n',
    }

    # Replace accented characters with their non-accented equivalents
    cleaned_str = ''.join(mapping.get(char, char) for char in input_str)

    return cleaned_str


class ImeaPagesGenerator(PagesGenerator):
    _pages_path = "assets", "pages"

    def _replace_common_assets(self, *page_source_path, save_name: str = None) -> str:
        page_path = os.path.join(*self._pages_path, *page_source_path)
        page = self._read(page_path)
        page = page.split("{{")
        page_parts = [page[0]]

        if len(page) != 1:
            for part in page[1:]:
                common_asset_id, content = part.split("}}")
                common_asset = self.common_assets[common_asset_id.rstrip().strip()]
                page_parts.append(common_asset)
                page_parts.append(content)

        page = remove_diacritics("".join(page_parts))
        if save_name:
            page_path = os.path.join(*self._pages_path, *page_source_path[:-1], save_name)
            self._save(page_path, page)
        return page

    def _default_generation(self, page_name: str, *page_path, folder: str = "Pages", save_name: str = None):
        self.pages[f"{folder}/{page_name}"] = self._replace_common_assets(*page_path, save_name=save_name)
        return self

    def relatorios(self):
        page = self._replace_common_assets("relatorio", "main.html", save_name="final.html").encode('utf-8')
        self.sharepoint_repository.upload_page("Relatorios.html", page, "Pages")
        return self

    def _relatiorios_detalhados_header(self):
        page = self._replace_common_assets("relatorio", "geral", "main.html", save_name="final.html").encode('utf-8')
        self.sharepoint_repository.upload_page("RelatoriosDetalhados.html", page, "Pages")
        return self

    def _relatiorios_detalhados_side_image(self):
        page = self._replace_common_assets("relatorio", "side-image", "main.html", save_name="final.html").encode(
            'utf-8')
        self.sharepoint_repository.upload_page("RelatoriosDetalhadosSideImage.html", page, "Pages")
        return self

    def relatorios_detalhados(self):
        return (self
                ._relatiorios_detalhados_header()
                ._relatiorios_detalhados_side_image()
                )

    def metodologia(self):
        return self._default_generation("Metodologia", "metodologia", "main.html")
