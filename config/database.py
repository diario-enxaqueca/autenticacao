"""Configuração do banco de dados usando SQLAlchemy (copiado do backend)."""
# Nome `SessionLocal` é uma convenção usada no projeto; pylint
# pode sinalizar `invalid-name` para variáveis em maiúsculas. Desabilitamos
# apenas para este arquivo.
# pylint: disable=invalid-name

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# import relativo para o pacote local de config
from .settings import settings


# URL de conexão do banco
DATABASE_URL = (
    f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}"
    f"@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/"
    f"{settings.MYSQL_DB}?ssl_mode={settings.MYSQL_SSL}"
)

# Engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
