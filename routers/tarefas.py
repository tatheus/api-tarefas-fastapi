from fastapi import APIRouter, Depends
from database import SessionLocal
from models import Tarefa, User
from schemas import TarefaCreate, TarefaResponse
from auth import verificar_token

router = APIRouter(prefix="/tarefas", tags=["Tarefa"])


@router.post("/")
def criar_tarefa(tarefa: TarefaCreate, payload=Depends(verificar_token)):
    db = SessionLocal()

    nova = Tarefa(
        titulo=tarefa.titulo,
        descricao=tarefa.descricao,
        usuario_id=int(payload["sub"]),
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)
    db.close()

    return nova


@router.get("/", response_model=list[TarefaResponse])
def listar_tarefas(payload=Depends(verificar_token)):
    db = SessionLocal()

    tarefas = db.query(Tarefa).filter(
        Tarefa.usuario_id == int(payload["sub"]),
    ).all()

    db.close()

    return tarefas


@router.put("/{tarefa_id}")
def atualizar_tarefa(
        tarefa_id: int,
        dados: TarefaCreate,
        payload=Depends(verificar_token),
):
        db = SessionLocal()

        tarefa = db.query(Tarefa).filter(
            Tarefa.id == int(payload["sub"]),
        ).first()

        if tarefa is None:
            db.close()
            return {"erro": "Tarefa não encontrada"}

        tarefa.titulo =dados.titulo
        tarefa.decricao = dados.descricao

        db.commit()
        db.refresh(tarefa)
        db.close()

        return tarefa


@router.delete("/{tarefa_id}")
def deletar_tarefa(
    tarefa_id: int,
    payload = Depends(verificar_token),
):
    db = SessionLocal()

    user_id = int(payload["sub"])

    tarefa = db.query(Tarefa).filter(
        Tarefa.id == tarefa_id,
        Tarefa.usuario_id == user_id,
    ).first()

    if tarefa is None:
        db.close()
        return {"erro": "Tarefa não encontrada"}

    db.delete(tarefa)
    db.commit()
    db.close()

    return {"mensagem": "tarefa removida"}

