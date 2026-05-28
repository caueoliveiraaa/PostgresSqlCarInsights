"""
Modelos Pydantic utilizados para mapear dados de exemplo em requisições.
"""

from pydantic import BaseModel, ConfigDict, Field


class ResponseExemplo(BaseModel):
    """
    Esquema de saída para representar os dados.
    """

    id: int = Field(
        ...,
        gt=0,
        description="Identificador do objeto",
    )

    descricao: str = Field(
        ...,
        max_length=100,
        description="Descrição do objeto",
    )

    ativo: bool = Field(
        ...,
        description="Se o objeto está ativo ou não",
    )

    class ConfigDict:
        from_attributes = True


class ResponseExemploPatch(BaseModel):
    """
    Esquema de saída para representar os dados em alterações.
    """

    descricao: str = Field(
        ...,
        max_length=100,
        description="Descrição do objeto",
    )

    ativo: bool = Field(
        ...,
        description="Se o objeto está ativo ou não",
    )

    class ConfigDict:
        from_attributes = True


class ConsultaExemplo(BaseModel):
    """
    Objeto que representa dados de exemplo quando o modelo ORM é
    convertido em um dicionário.
    """

    model_config = ConfigDict(frozen=False, str_strip_whitespace=True)

    id: int = Field(
        ...,
        gt=0,
        description="Identificador do objeto",
    )

    descricao: str = Field(
        ...,
        max_length=100,
        description="Descrição do objeto",
    )

    ativo: bool = Field(
        ...,
        description="Se o objeto está ativo ou não",
    )
