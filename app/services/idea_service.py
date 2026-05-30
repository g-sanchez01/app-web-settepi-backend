from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

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