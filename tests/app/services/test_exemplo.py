"""
Testes para a classe ConsultorDados.
"""

import pytest

from app.schemas.exemplo import ConsultaExemplo
from app.services.exemplo import ConsultorDados


class TestesConsultorDados:
    """
    Classe responsável por testar a o consultor de dados.
    """

    @pytest.fixture(autouse=True)
    def setup(self, consultor_dados: ConsultorDados) -> None:
        """
        Inicializa o serviço de validação real.
        """
        self.consultor = consultor_dados

    async def test_consulta_dados_mock(self) -> None:
        """
        Valida se o mock fixo retorna os valores esperados.
        """
        resultado = await self.consultor.consulta_dados_mock()

        assert isinstance(resultado, ConsultaExemplo)
        assert resultado.id == 1
        assert resultado.descricao == "string"
        assert resultado.ativo is True

    async def test_gera_dados_mock(self) -> None:
        """
        Valida o espelhamento de dados (echo) do método gera_dados.
        """
        id_alvo = 10
        dados_entrada = ConsultaExemplo(id=id_alvo, descricao="info", ativo=False)

        resultado = await self.consultor.gera_dados_mock(dados_entrada)

        assert resultado.id == id_alvo
        assert resultado.descricao == "info"
        assert resultado is dados_entrada

    async def test_modifica_dados_mock(self) -> None:
        """
        Valida se o ID é corretamente sobrescrito conforme a regra do método.
        """
        id_novo = 99
        dados_originais = ConsultaExemplo(id=1, descricao="desc", ativo=True)

        resultado = await self.consultor.modifica_dados_mock(
            dados_originais, id_novo
        )

        assert resultado.id == id_novo
        assert resultado.descricao == "desc"
        assert resultado.ativo is True

    async def test_remove_dados_mock(self) -> None:
        """
        Valida se a "remoção" mockada retorna o objeto com o ID solicitado.
        """
        id_alvo = 500

        resultado = await self.consultor.remove_dados_mock(id_alvo)

        assert resultado.id == id_alvo
        assert isinstance(resultado, ConsultaExemplo)
