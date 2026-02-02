from fastapi.security import OAuth2PasswordRequestForm
from schemas import UsuarioCreate, UsuarioLogin, TokenResponse
from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from models import User
from security import gerar_hash_senha, verificar_senha
from auth import criar_token, verificar_token

router = APIRouter()

@router.post("/usuarios")
def criar_usuario(usuario: UsuarioCreate):
    db = SessionLocal()
    try:
        senha_hash = gerar_hash_senha(usuario.senha)

        usuario_db = User(
            nome=usuario.nome,
            email=usuario.email,
            senha=senha_hash
        )

        db.add(usuario_db)
        db.commit()
        db.refresh(usuario_db)

        return {
            "id": usuario_db.id,
            "nome": usuario_db.nome,
            "email": usuario_db.email
        }
    finally:
        db.close()


@router.get("/usuarios")
def listar_usuarios():
    db = SessionLocal()

    usuarios = db.query(User).all()

    db.close()
    return usuarios


@router.get("/usuarios/{usuario_id}")
def buscar_usuario(usuario_id: int):
    db = SessionLocal()

    usuario = db.query(User).filter(User.id == usuario_id).first()

    db.close()

    if usuario is None:
        return {"erro": "Usuário não encontrado"}

    return usuario


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()

    usuario = db.query(User).filter(
        User.email == form_data.username
    ).first()

    db.close()

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(status_code=401, detail="Senha incorreta")

    token = criar_token({"sub": str(usuario.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/rota-protegida")
def rota_protegida(payload = Depends(verificar_token)):
    return {"mensagem": "acesso autorizado"}
