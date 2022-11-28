from typing import Optional
from pydantic import BaseModel

class CursoS(BaseModel):
    id: Optional[int]
    nombre: str
    profesor: str
    creditos: int
    ciclo: int
    alumnos: Optional[str]

    class Config:
        orm_mode = True