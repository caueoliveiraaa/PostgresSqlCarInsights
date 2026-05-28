"""
Classe que representa uma exceção de configuração inválida.
"""


class InvalidConfigError(Exception):
    """
    Erro para configuração inválida identificada.
    """

    def __init__(
        self, message: str = "A configuração fornecida é inválida!"
    ) -> None:
        """
        Construtor da exceção responsável pela validação da configuração do projeto.
        """
        super().__init__(message)
