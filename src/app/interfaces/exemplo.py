"""
Armazena a interface de contrato para a lógica que serve como exemplo
de implementação.
"""

from abc import ABC, abstractmethod

from app.schemas.exemplo import ConsultaExemplo


class IConsultorDados(ABC):
    """
    Interface que define o contrato para o serviço de Consultor de Dados.
    """

    @abstractmethod
    async def consulta_dados_mock(self) -> ConsultaExemplo:
        """
        Contrato para consulta de dados de exemplo.
        """
        pass

    @abstractmethod
    async def gera_dados_mock(
        self, dados_exemplo: ConsultaExemplo
    ) -> ConsultaExemplo:
        """
        Contrato para geração de dados de exemplo.
        """
        pass

    @abstractmethod
    async def modifica_dados_mock(
        self, dados_exemplo: ConsultaExemplo, id_exemplo: int
    ) -> ConsultaExemplo:
        """
        Contrato para modificação de dados de exemplo.
        """
        pass

    @abstractmethod
    async def remove_dados_mock(self, id_exemplo: int) -> ConsultaExemplo:
        """
        Contrato para remoção de dados de exemplo.
        """
        pass
