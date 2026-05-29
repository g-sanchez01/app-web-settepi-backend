from sqlalchemy.orm import Session
from datetime import datetime

from app.models.idea_formulario import IdeaFormulario
from app.schemas.idea import IdeaCreate
from app.schemas.user_token import UserToken
from app.utils.datetime_utils import now_mexico


def crear_idea(
    data: IdeaCreate,
    user: UserToken,
    db: Session
):

    nueva_idea = IdeaFormulario(
        
        nombre=user.nombre,
        nomina=user.numero_nomina,
        telefono= user.telefono,
        departamento=user.departamento,

        unidadNegocio=data.unidadNegocio,
        zona=data.zona,
        tituloIdea=data.tituloIdea,
        descripcionIdea=data.descripcionIdea,

        fecha=now_mexico()
    )

    db.add(nueva_idea)
    db.commit()
    db.refresh(nueva_idea)

    return nueva_idea