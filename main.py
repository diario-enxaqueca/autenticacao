from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import router do pacote auth (imports absolutos necessários para execução
# quando `main.py` é carregado como módulo top-level por uvicorn)
from auth.view_auth import router as auth_router
from config.settings import settings

app = FastAPI(title="Autenticação - Diário de Enxaqueca",
              version="1.0.0",
              debug=settings.DEBUG)

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


@app.get("/health")
def health():
    return {"status": "healthy"}
