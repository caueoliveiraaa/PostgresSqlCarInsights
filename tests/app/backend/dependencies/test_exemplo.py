"""
Testes para a dependência de consultor de dados.
"""

from app.backend.dependencies.exemplo import injeta_consultor
from app.services.exemplo import ConsultorDados


async def test_injeta_consultor() -> None:
    """
    Garante que retorna uma instância de ConsultorDados.
    """
    consultor = await injeta_consultor()

    assert isinstance(consultor, ConsultorDados)
