from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer
from config.db import Base

class CursoM(Base):
    __tablename__ = "Cursos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(30))
    profesor = Column(String(30))
    creditos = Column(Integer)
    ciclo = Column(Integer)
    alumnos = Column(String(300))