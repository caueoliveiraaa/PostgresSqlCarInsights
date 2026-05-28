"""
Modelo de dados para a tabela user_auth, utilizada na autenticação via JWT.
"""

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_api.base_declarativa import BaseModelsApi


class UserAuth(BaseModelsApi):
    """Mapeamento da tabela user_auth."""

    __tablename__ = "user_auth"
    __table_args__ = {"extend_existing": True, "schema": "dbo"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    username: Mapped[str] = mapped_column(String(150), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    api_name: Mapped[str] = mapped_column(String(55), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=True)
