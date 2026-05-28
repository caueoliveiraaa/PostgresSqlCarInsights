"""
Modelo Pydantic utilizado nas rotas de testes para validação do
funcionamento do projeto.
"""

from pydantic import BaseModel, Field


class HealthCheck(BaseModel):
    """
    Modelo de recebimento de dados para endpoints de testes.
    """

    texto_teste: str = Field(
        ...,
        max_length=100,
        description="Campo de string para validação de conectividade",
    )

    inteiro_teste: int = Field(
        ...,
        gt=0,
        description="Campo numérico positivo para validação de tipos de dados",
    )
