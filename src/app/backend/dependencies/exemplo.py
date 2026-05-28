"""
Dependência para consultor de dados (exemplo de implementação).
"""

from beartype import beartype

from app.services.exemplo import ConsultorDados


@beartype
async def injeta_consultor() -> ConsultorDados:
    """
    Retorna uma instância da classe que consulta dados como exemplo.
    """
    return ConsultorDados()
