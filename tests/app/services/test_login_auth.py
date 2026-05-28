"""
Testes para serviços de autenticação de usuários.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.settings import Settings
from app.models.base_api.user_auth import UserAuth
from app.services.login_auth import (
    ManipuladorHashService,
    ManipuladorTokenService,
    ManipuladorUsuarioService,
    ValidadorTokenService,
)


class TestesValidadorTokenService:
    """
    Classe responsável por testar a integração com a biblioteca python-jose.
    """

    @pytest.fixture(autouse=True)
    def setup(self, validador_token: ValidadorTokenService) -> None:
        """
        Inicializa o serviço de validação real.
        """
        self.validador = validador_token
        self.secret = "test_secret"
        self.algorithm = "HS256"
        self.payload = {"sub": "123"}

    def test_encode_token_sucesso(self) -> None:
        """
        Garante que o serviço consegue gerar uma string JWT válida.
        """
        divisoes = 3

        token = self.validador.encode(self.payload, self.secret, self.algorithm)

        assert isinstance(token, str)
        assert len(token.split(".")) == divisoes

    def test_decode_token_sucesso(self) -> None:
        """
        Garante que o serviço consegue decodificar um token e extrair os
        dados originais.
        """
        token = self.validador.encode(self.payload, self.secret, self.algorithm)

        resultado = self.validador.decode(token, self.secret, [self.algorithm])

        assert resultado["sub"] == self.payload["sub"]


class TestesManipuladorHashService:
    """
    Classe responsável por testar a integração com a lógica de hash do Werkzeug.
    """

    @pytest.fixture(autouse=True)
    def setup(self, manipulador_hash: ManipuladorHashService) -> None:
        """
        Inicializa o serviço de hash real.
        """
        self.hasher = manipulador_hash
        self.senha_pura = "minha_senha"

    def test_gera_hash_diferente_da_senha(self) -> None:
        """
        Garante que a senha é transformada e não armazenada em texto claro.
        """
        hash_gerado = self.hasher.gera_hash(self.senha_pura)

        assert hash_gerado != self.senha_pura

    def test_valida_hash_correto(self) -> None:
        """
        Garante que a validação retorna True para a combinação correta de senha
        e hash.
        """
        hash_gerado = self.hasher.gera_hash(self.senha_pura)
        valido = self.hasher.valida_hash(hash_gerado, self.senha_pura)

        assert valido is True

    def test_valida_hash_incorreto(self) -> None:
        """
        Garante que a validação retorna False para senhas divergentes do hash.
        """
        hash_gerado = self.hasher.gera_hash(self.senha_pura)
        invalido = self.hasher.valida_hash(hash_gerado, "senha_errada")

        assert invalido is False

    def test_hashes_sao_unicos_para_mesma_senha(self) -> None:
        """
        Garante que o serviço gera hashes diferentes para a mesma senha.
        """
        hash_1 = self.hasher.gera_hash(self.senha_pura)
        hash_2 = self.hasher.gera_hash(self.senha_pura)

        assert hash_1 != hash_2


@pytest.mark.asyncio
class TestesManipuladorTokenService:
    """
    Classe responsável por testar a classe ManipuladorTokenService.
    """

    @pytest.fixture(autouse=True)
    def setup(
        self,
        manipulador_token: ManipuladorTokenService,
    ) -> None:
        """
        Inicializa objetos mocados para testes.
        """
        self.manipulador = manipulador_token

    async def test_cria_e_decodifica_token(self) -> None:
        """
        Garante que um token criado pode ser lido e contém o 'sub' correto.
        """
        sub_esperado = "usuario_123"

        token = await self.manipulador.cria_token_acesso(sub_esperado)
        payload = await self.manipulador.decodifica_token(token)

        assert payload.sub == sub_esperado

    async def test_decodifica_token_invalido(self) -> None:
        """
        Garante que um erro 401 é lançado para tokens malformados.
        """
        status_esperado = status.HTTP_401_UNAUTHORIZED
        with pytest.raises(HTTPException) as erro:
            await self.manipulador.decodifica_token("token_que_nao_existe")

        assert erro.value.status_code == status_esperado


@pytest.mark.asyncio
class TestesManipuladorUsuarioService:
    """
    Classe responsável por testar a classe ManipuladorUsuarioService.
    """

    @pytest.fixture(autouse=True)
    def setup(
        self,
        manipulador_usuario: ManipuladorUsuarioService,
        mock_settings: Settings,
        mock_repo_usuarios: MagicMock,
    ) -> None:
        """
        Inicializa objetos mocados para testes.
        """
        self.manipulador = manipulador_usuario
        self.mock_repo = mock_repo_usuarios

    async def test_autentica_usuario(self) -> None:
        """
        Garante a autenticação com usuário ativo e senha correta.
        """
        form = MagicMock(
            username="user", password="123", spec=OAuth2PasswordRequestForm
        )
        usuario_db = UserAuth(username="user", ativo=True, password_hash="hash_123")
        self.mock_repo.busca_por_username = AsyncMock(return_value=usuario_db)

        resultado = await self.manipulador.autentica_usuario(form)

        assert resultado == usuario_db

    async def test_autentica_usuario_falha(self) -> None:
        """
        Garante erro 401 se a senha não bater com o hash.
        """
        status_esperado = status.HTTP_401_UNAUTHORIZED
        form = MagicMock(
            username="user", password="123", spec=OAuth2PasswordRequestForm
        )
        usuario_db = UserAuth(username="user", ativo=False, password_hash="hash_123")
        self.mock_repo.busca_por_username = AsyncMock(return_value=usuario_db)

        with pytest.raises(HTTPException) as erro:
            await self.manipulador.autentica_usuario(form)

        assert erro.value.status_code == status_esperado

    async def test_autentica_usuario_admin(self) -> None:
        """
        Garante que um usuário is_admin=True passa na validação de admin.
        """
        usuario_admin = UserAuth(
            username="admin_user",
            is_admin=True,
            password_hash="hash_123",
            ativo=True,
        )
        form = MagicMock(
            username="admin_user", password="123", spec=OAuth2PasswordRequestForm
        )
        self.mock_repo.busca_admin = AsyncMock(return_value=usuario_admin)

        resultado = await self.manipulador.autentica_usuario_admin(form)

        assert resultado == usuario_admin

    async def test_autentica_usuario_admin_falha(self) -> None:
        """
        Garante que um usuário is_admin=False não passa na validação de admin.
        """
        status_esperado = status.HTTP_401_UNAUTHORIZED
        usuario_admin = UserAuth(
            username="comum", is_admin=False, password_hash="hash_123"
        )
        form = MagicMock(
            username="comum", password="123", spec=OAuth2PasswordRequestForm
        )
        self.mock_repo.busca_admin = AsyncMock(return_value=usuario_admin)

        with pytest.raises(HTTPException) as erro:
            await self.manipulador.autentica_usuario_admin(form)

        assert erro.value.status_code == status_esperado

    async def test_cria_novo_usuario(self) -> None:
        """
        Garante a execução do fluxo de criação de um usuário novo do sistema.
        """
        self.mock_repo.busca_por_username = AsyncMock(return_value=None)
        self.mock_repo.salva_usuario = AsyncMock()

        await self.manipulador.cria_novo_usuario("novo", "senha123")

        self.mock_repo.salva_usuario.assert_called_once()

    async def test_cria_novo_usuario_falha(self) -> None:
        """
        Garante erro 400 ao tentar criar usuário com nome já ocupado.
        """
        status_esperado = status.HTTP_400_BAD_REQUEST
        usuario_db = UserAuth(username="user", ativo=True, password_hash="hash_123")
        self.mock_repo.busca_por_username = AsyncMock(return_value=usuario_db)
        self.mock_repo.salva_usuario = AsyncMock()

        with pytest.raises(HTTPException) as erro:
            await self.manipulador.cria_novo_usuario("user", "senha")

        self.mock_repo.salva_usuario.assert_not_called()
        assert erro.value.status_code == status_esperado

    async def test_cria_novo_usuario_admin(self) -> None:
        """
        Garante a execução do fluxo de criação do primeiro admin do sistema.
        """
        self.mock_repo.busca_admin = AsyncMock(return_value=None)
        self.mock_repo.salva_usuario = AsyncMock()

        await self.manipulador.cria_novo_usuario_admin()

        self.mock_repo.salva_usuario.assert_called_once()

    async def test_cria_novo_usuario_admin_falha(self) -> None:
        """
        Garante erro 400 ao tentar criar usuário admin quando o mesmo já existe.
        """
        status_esperado = status.HTTP_400_BAD_REQUEST
        usuario_admin = UserAuth(
            username="comum", is_admin=False, password_hash="hash_123"
        )
        self.mock_repo.busca_admin = AsyncMock(return_value=usuario_admin)
        self.mock_repo.salva_usuario = AsyncMock()

        with pytest.raises(HTTPException) as erro:
            await self.manipulador.cria_novo_usuario_admin()

        self.mock_repo.salva_usuario.assert_not_called()
        assert erro.value.status_code == status_esperado
