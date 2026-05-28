"""
Modelo Pydantic utilizado nas rotas e serviços de autenticação da API.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class JwtTokenResponse(BaseModel):
    """
    Modelo de resposta para o token JWT gerado após login.
    """

    access_token: str = Field(
        ...,
        min_length=5,
        max_length=255,
        description="Token JWT de acesso",
    )
    token_type: str = Field(
        ...,
        min_length=5,
        max_length=255,
        description="Tipo do token (geralmente 'bearer')",
    )


class UsuarioResponse(BaseModel):
    """
    Modelo de resposta para criação de novos usuários no banco de dados.
    """

    message: str = Field(
        ...,
        min_length=5,
        max_length=255,
        description="Mensagem de sucesso após criação de usuários",
    )


class TokenEncode(BaseModel):
    """
    Payload para manipulação de tokens da biblioteca python-jose via método
    encode.
    """

    sub: str = Field(
        ...,
        max_length=255,
        description="Identificador único do usuário do token",
    )

    iat: datetime = Field(
        ...,
        description="Data e hora em que o token foi emitido",
    )

    exp: datetime = Field(
        ...,
        description="Data e hora em que o token expira e deixa de ser válido",
    )


class TokenDecode(BaseModel):
    """
    Payload para manipulação de tokens da biblioteca python-jose via método
    decode.
    """

    sub: str = Field(
        ...,
        max_length=255,
        description="Identificador único do usuário do token",
    )

    iat: int = Field(
        ...,
        description="Momento em que o token foi emitido",
    )

    exp: int = Field(
        ...,
        description="Momento em que o token expira e deixa de ser válido",
    )
