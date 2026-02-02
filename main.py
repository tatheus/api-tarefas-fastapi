from fastapi import FastAPI
from database import engine, Base
from routers import usuarios, tarefas
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(usuarios.router)
app.include_router(tarefas.router)

@app.get("/")
def home():
    return {"mensagem": "Backend rodando!"}

