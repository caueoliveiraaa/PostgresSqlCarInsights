"""
Testes para a classe UsuariosRepository.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.base_api.user_auth import UserAuth
from app.repositories.usuarios import UsuariosRepository


@pytest.mark.asyncio
class TestesUsuariosRepository:
    """
    Classe responsável por testar a camada de repositório de usuários,
    garantindo a correta execução de queries SQLAlchemy.
    """

    @pytest.fixture(autouse=True)
    def setup(
        self, mock_sessao: MagicMock, usuarios_repository: UsuariosRepository
    ) -> None:
        """
        Inicializa o repositório com uma sessão assíncrona mocada.
        """
        self.mock_sessao = mock_sessao
        self.repo = usuarios_repository
        self.api_name = "api_teste"

    async def test_busca_por_username_sucesso(self) -> None:
        """
        Garante que a query de busca por username retorna o usuário correto.
        """
        username = "nome"
        usuario_esperado = UserAuth(username=username, api_name=self.api_name)

        mock_result = MagicMock()
        self.mock_sessao.execute = AsyncMock(return_value=mock_result)
        mock_result.scalars.return_value.first.return_value = usuario_esperado

        resultado = await self.repo.busca_por_username(username, self.api_name)

        assert resultado is not None
        assert resultado == usuario_esperado
        assert resultado.username == username
        self.mock_sessao.execute.assert_called_once()

    async def test_busca_admin_sucesso(self) -> None:
        """
        Garante que a query de busca por administrador filtra corretamente pelo
        campo is_admin.
        """
        admin_esperado = UserAuth(
            username="admin", is_admin=True, api_name=self.api_name
        )

        mock_result = MagicMock()
        self.mock_sessao.execute = AsyncMock(return_value=mock_result)
        mock_result.scalars.return_value.first.return_value = admin_esperado

        resultado = await self.repo.busca_admin(self.api_name)

        assert resultado is not None
        assert resultado == admin_esperado
        assert resultado.is_admin is True
        self.mock_sessao.execute.assert_called_once()

    async def test_salva_usuario_executa_fluxo_completo(self) -> None:
        """
        Garante que o fluxo de salvar (add, commit, refresh) é executado na sessão.
        """
        novo_usuario = UserAuth(username="novo", api_name=self.api_name)
        self.mock_sessao.commit = AsyncMock()
        self.mock_sessao.refresh = AsyncMock()

        await self.repo.salva_usuario(novo_usuario)

        self.mock_sessao.add.assert_called_once_with(novo_usuario)
        self.mock_sessao.commit.assert_called_once()
        self.mock_sessao.refresh.assert_called_once_with(novo_usuario)
