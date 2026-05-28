"""
Lógica para as consultas de dados e regras de negócio.
"""

from beartype import beartype

from app.interfaces.exemplo import IConsultorDados
from app.schemas.exemplo import ConsultaExemplo


class ConsultorDados(IConsultorDados):
    """
    Classe que serve de exemplo para implementação de regras de negócio.
    """

    @beartype
    async def consulta_dados_mock(self) -> ConsultaExemplo:
        """
        Consulta dados como exemplo.
        """
        return ConsultaExemplo(
            id=1,
            descricao="string",
            ativo=True,
        )

    @beartype
    async def gera_dados_mock(
        self, dados_exemplo: ConsultaExemplo
    ) -> ConsultaExemplo:
        """
        Retorna dados gerados como exemplo.
        """
        return dados_exemplo

    @beartype
    async def modifica_dados_mock(
        self, dados_exemplo: ConsultaExemplo, id_exemplo: int
    ) -> ConsultaExemplo:
        """
        Retorna dados modificados como exemplo.
        """
        dados_exemplo.id = id_exemplo
        dados_exemplo.descricao = dados_exemplo.descricao
        dados_exemplo.ativo = dados_exemplo.ativo
        return dados_exemplo

    @beartype
    async def remove_dados_mock(self, id_exemplo: int) -> ConsultaExemplo:
        """
        Retorna dados deletados como exemplo.
        """
        return ConsultaExemplo(
            id=id_exemplo,
            descricao="string",
            ativo=True,
        )
