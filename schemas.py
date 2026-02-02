from pydantic import BaseModel


class TarefaCreate(BaseModel):
    titulo: str
    descricao: str


class TarefaResponse(BaseModel):
    id: int
    titulo: str
    descricao: str
    usuario_id: int

    class Config:
        from_attributes = True


class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str


class UsuarioLogin(BaseModel):
    email: str
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        from_attributes = True