from src.service.imea_pages_generator import ImeaPagesGenerator

generator = ImeaPagesGenerator()
(
    generator
    # .generate_relatorio()
    .generate_relatorios()
    .generate_pages()
)
