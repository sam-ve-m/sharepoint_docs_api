from src.repository.sharepoint import Sharepoint
from src.service.imea_pages_generator import ImeaPagesGenerator

repo = Sharepoint()

generator = ImeaPagesGenerator()
(
    generator
    .relatorios()
    # .relatorios_detalhados()
    .generate_pages()
)
