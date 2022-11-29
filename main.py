from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from fastapi import Request, Depends, Request, Form
from config.db import SessionLocal, engine
import model.curso_model
from sqlalchemy.orm import Session
from model.curso_model import CursoM

model.curso_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/curso/{id}", response_class=HTMLResponse)
def get_curso_id(request: Request, id: int, db: Session = Depends(get_database_session)):
    curso = db.query(CursoM).filter(CursoM.id == id).first()
    return templates.TemplateResponse("view_curso.html", {"request": request, "curso": curso})

@app.get("/curso", response_class=HTMLResponse)
def get_curso_all(request: Request, db: Session = Depends(get_database_session)):
    cursos = db.query(CursoM).all()
    return templates.TemplateResponse("list_curso.html", {"request": request, "curso_list": cursos})

@app.get("/create_curso_ui", response_class=HTMLResponse)
async def create_curso_ui(request: Request):
    return templates.TemplateResponse("create_curso.html", {"request": request})

@app.post("/create_curso/", response_class=HTMLResponse)
def create_curso(nombre: str = Form(...), profesor: str = Form(...), creditos: int = Form(...), ciclo: int = Form(...), db: Session = Depends(get_database_session)):
    curso = CursoM(nombre=nombre, profesor=profesor, creditos=creditos, ciclo=ciclo)
    db.add(curso)
    db.commit()
    return RedirectResponse(url="/curso", status_code=303)

@app.get("/asignar_curso_ui", response_class=HTMLResponse)
async def asignar_curso_ui(request: Request):
    return templates.TemplateResponse("asignar_curso.html", {"request": request})

@app.post("/asignar_curso", response_class=HTMLResponse)
def asignar_curso(id_curso: int = Form(...), id_alumno: int = Form(...), db: Session = Depends(get_database_session)):
    curso = db.query(CursoM).filter(CursoM.id == id_curso).first()
    update = ''
    if curso.alumnos is None:
        update =  str(id_alumno)
    else:
        update = "'"+curso.alumnos + "|" + str(id_alumno)+"'"
    db.query(CursoM).filter(CursoM.id == id_curso).update({CursoM.alumnos: update})
    db.commit()
    cursos = 0;
    asignacion = db.execute("SELECT a.cursos FROM Alumnos.Alumnos a WHERE id = " + str(id_alumno)).fetchone()
    if asignacion[0] is None:
        cursos = 1
    else:
        cursos = asignacion[0] +1
    db.execute("UPDATE Alumnos.Alumnos a SET a.cursos = "+str(cursos)+ " WHERE id = "+str(id_alumno))
    db.commit()
    return RedirectResponse(url="/curso", status_code=303)

@app.get("/curso/delete/{id}", response_class=HTMLResponse)
def delete_curso(id: int, db: Session = Depends(get_database_session)):
    db.query(CursoM).filter(CursoM.id == id).delete()
    db.commit()
    return RedirectResponse(url="/curso", status_code=303)

@app.get("/curso/update/{id}", response_class=HTMLResponse)
def update_curso(id: int, request: Request, db: Session = Depends(get_database_session)):
    result = db.query(CursoM).filter(CursoM.id == id).first()
    return templates.TemplateResponse("update_curso.html", {"request": request, "curso": result})

@app.post("/update_curso", response_class=HTMLResponse)
def update_curso(request: Request, id: int = Form(...), profesor: str = Form(...), creditos: int  = Form(...), db: Session = Depends(get_database_session)):
    db.query(CursoM).filter(CursoM.id == id).update({CursoM.profesor: profesor, CursoM.creditos: creditos})
    db.commit()
    return RedirectResponse(url="/curso", status_code=303)