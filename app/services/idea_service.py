from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import date

from app.models.idea_formulario import IdeaFormulario
from app.models.colaborador import Colaborador
from app.schemas.idea import IdeaCreate
from app.utils.datetime_utils import now_mexico

from app.repositories.idea_repository import IdeaRepository


def crear_idea(data: IdeaCreate, user: Colaborador, db: Session):

    nueva_idea = IdeaFormulario(
        nombre=user.nombre,
        nomina=user.numero_nomina,
        telefono=user.telefono,
        departamento=user.departamento,

        unidadNegocio=data.unidadNegocio,
        zona=data.zona,
        tituloIdea=data.tituloIdea,
        descripcionIdea=data.descripcionIdea,

        fecha=now_mexico()
    )

    return IdeaRepository.crear_idea(db, nueva_idea)

def editar_idea(db, id_idea, data):

    idea = IdeaRepository.obtener_por_id(db, id_idea)

    if not idea:
        raise HTTPException(status_code=404, detail="Idea no encontrada")

    if idea.estado != "BORRADOR":
        raise HTTPException(
            status_code=400,
            detail="Solo se puede editar en BORRADOR"
        )

    return IdeaRepository.actualizar_idea(db, idea, data)


def enviar_idea(db: Session, id_idea: int):

    idea = IdeaRepository.obtener_por_id(
        db,
        id_idea
    )

    if not idea:
        raise HTTPException(
            status_code=404,
            detail="Idea no encontrada"
        )

    if idea.estado != "BORRADOR":
        raise HTTPException(
            status_code=400,
            detail="Solo se pueden enviar ideas en BORRADOR"
        )

    return IdeaRepository.enviar_idea(
        db,
        idea
    )

def obtener_ideas(
    db: Session,
    user: Colaborador,
    idRegistroIdea: str | None = None,
    nombre: str | None = None,
    nomina: str | None = None,
    telefono: str | None = None,
    unidadNegocio: str | None = None,
    zona: str | None = None,
    departamento: str | None = None,
    tituloIdea: str | None = None,
    estado: str | None = None,
    fecha: date | None = None
):
    # Administrador: ve todas las ideas
    if user.rol == "GESTOR":
        return IdeaRepository.obtener_todas(
            db=db,
            idRegistroIdea=idRegistroIdea,
            nombre=nombre,
            nomina=nomina,
            telefono=telefono,
            unidadNegocio=unidadNegocio,
            zona=zona,
            departamento=departamento,
            tituloIdea=tituloIdea,
            estado="ENVIADA",
            fecha=fecha
        )
    
    # Usuario General
    return IdeaRepository.obtener_por_nomina(
        db=db,
        nomina=user.numero_nomina,
        idRegistroIdea=idRegistroIdea,
        tituloIdea=tituloIdea,
        estado=estado,
        fecha=fecha
    )