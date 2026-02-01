from fastapi import FastAPI
from database import engine, Base
from routers import usuarios, tarefas


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(usuarios.router)

app.include_router(tarefas.router)

@app.get("/")
def home():
    return {"mensagem": "Backend rodando!"}
