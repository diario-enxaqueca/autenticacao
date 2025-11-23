import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

# Import router do pacote auth (imports absolutos necessários para execução
# quando `main.py` é carregado como módulo top-level por uvicorn)
from auth.view_auth import router as auth_router
from config.settings import settings
from config.database import Base, engine

logger = logging.getLogger("uvicorn")

app = FastAPI(
    title="Autenticação - Diário de Enxaqueca",
    version="1.0.0",
    debug=settings.DEBUG,
)

origins = [
    "http://localhost:3000",
    "http://frontend",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])


@app.on_event("startup")
def startup_event():
    """Cria tabelas ao iniciar (se não existirem).
    
    create_all() usa CREATE TABLE IF NOT EXISTS, então:
    - Não apaga dados existentes
    - Garante que tabelas existam em qualquer restart
    - init.sql ainda é responsável pelos INSERTs iniciais
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas auth verificadas/criadas")
    except OperationalError as exc:
        logger.error("Erro ao criar tabelas: %s", exc)


@app.get("/health")
def health():
    return {"status": "healthy"}
