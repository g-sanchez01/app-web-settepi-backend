from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.models.colaborador_mes import ColaboradorMes

class ColaboradorMesRepository:

    @staticmethod
    def asignar(db: Session, numero_nomina: int, departamento: str):

        now = datetime.now()

       # validar si ya existe
        existente = db.query(ColaboradorMes).filter(
            ColaboradorMes.departamento == departamento,
            ColaboradorMes.mes == now.month,
            ColaboradorMes.anio == now.year
        ).first() 

        if existente:
            return None
        
        new = ColaboradorMes(
            numero_nomina=numero_nomina,
            departamento=departamento,
            mes=now.month,
            anio=now.year
        )

        db.add(new)
        db.commit()
        db.refresh(new)

        return new