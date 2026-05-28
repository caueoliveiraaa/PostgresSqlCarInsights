"""
Exemplo de rotas para consulta de dados.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.backend.dependencies.exemplo import injeta_consultor
from app.backend.dependencies.login_auth import injeta_autenticacao_jwt
from app.schemas.exemplo import (
    ConsultaExemplo,
    ResponseExemplo,
    ResponseExemploPatch,
)
from app.services.exemplo import ConsultorDados

router_exemplo = APIRouter(prefix="", tags=["Exemplo"])

DepAuthToken = Annotated[dict[str, str], Depends(injeta_autenticacao_jwt)]
DepConsultor = Annotated[ConsultorDados, Depends(injeta_consultor)]


@router_exemplo.get(
    "/exemplo-protegido",
    response_model=ResponseExemplo,
    status_code=status.HTTP_200_OK,
)
async def busca_dados_exemplo_protegido(
    _payload: DepAuthToken, consultor: DepConsultor
) -> ResponseExemplo:
    """
    Simula recuperação do exemplo de dados para requisições GET com proteção JWT.
    """
    dados: ConsultaExemplo = await consultor.consulta_dados_mock()
    return ResponseExemplo.model_validate(dados, from_attributes=True)


@router_exemplo.get(
    "/exemplo",
    response_model=ResponseExemplo,
    status_code=status.HTTP_200_OK,
)
async def busca_dados_exemplo(consultor: DepConsultor) -> ResponseExemplo:
    """
    Simula recuperação do exemplo de dados para requisições GET.
    """
    dados: ConsultaExemplo = await consultor.consulta_dados_mock()
    return ResponseExemplo.model_validate(dados, from_attributes=True)


@router_exemplo.post(
    "/exemplo",
    response_model=ResponseExemplo,
    status_code=status.HTTP_201_CREATED,
)
async def cria_exemplo(
    dados_exemplo: ResponseExemplo, consultor: DepConsultor
) -> ResponseExemplo:
    """
    Simula criação do exemplo de dados para requisições POST.
    """
    objeto = ConsultaExemplo(**dados_exemplo.model_dump())
    dados: ConsultaExemplo = await consultor.gera_dados_mock(objeto)
    return ResponseExemplo.model_validate(dados, from_attributes=True)


@router_exemplo.patch(
    "/exemplo/{id_exemplo}",
    response_model=ResponseExemplo,
    status_code=status.HTTP_200_OK,
)
async def altera_exemplo(
    id_exemplo: int, dados_exemplo: ResponseExemploPatch, consultor: DepConsultor
) -> ResponseExemplo:
    """
    Simula alteração do exemplo de dados para requisições PATCH.
    """
    objeto = ConsultaExemplo(id=id_exemplo, **dados_exemplo.model_dump())
    dados: ConsultaExemplo = await consultor.modifica_dados_mock(objeto, id_exemplo)
    return ResponseExemplo.model_validate(dados, from_attributes=True)


@router_exemplo.delete(
    "/exemplo/{id_exemplo}",
    status_code=status.HTTP_200_OK,
)
async def deleta_exemplo(
    id_exemplo: int, consultor: DepConsultor
) -> ResponseExemplo:
    """
    Simula exclusão do exemplo de dados para requisições DELETE.
    """
    dados: ConsultaExemplo = await consultor.remove_dados_mock(id_exemplo)
    return ResponseExemplo.model_validate(dados, from_attributes=True)
