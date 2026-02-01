from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha = Column(String)

    tarefas = relationship("Tarefa", back_populates="usuario")


class Tarefa(Base):
    __tablename__ = "tarefa"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    descricao = Column(String)

    usuario_id = Column(Integer, ForeignKey("users.id"))

    usuario = relationship("User", back_populates="tarefas")

