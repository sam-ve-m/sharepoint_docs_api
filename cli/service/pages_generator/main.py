from cli.repository.sharepoint import Sharepoint
from cli.service.pages_generator.imea_pages_generator import ImeaPagesGenerator


if __name__ == "__main__":
    repo = Sharepoint()

    generator = ImeaPagesGenerator()
    (
        generator
        .relatorios()
        .relatorios_detalhados()
        .generate_pages()
    )
