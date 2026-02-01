from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def gerar_hash(senha: str):
    senha = senha[:72]  # limite do bcrypt
    return pwd_context.hash(senha)

def verificar_senha(senha: str, hash_salvo: str):
    return pwd_context.verify(senha, hash_salvo)