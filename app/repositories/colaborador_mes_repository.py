from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from app.models.colaborador_mes import ColaboradorMes
from app.models.colaborador import Colaborador


class ColaboradorMesRepository:

    @staticmethod
    def crear_solicitud(db: Session, data: ColaboradorMes):

        ya_existe = ColaboradorMesRepository.existe_asignacion_mes(
            db,
            data.departamento,
            data.mes,
            data.anio
        )

        if ya_existe:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un colaborador del mes para este periodo"
            )

        try:
            db.add(data)
            db.commit()
            db.refresh(data)
            return data

        except Exception as e:
            db.rollback()
            raise e
        
    # ==============================
    # APROBAR Y ASIGNAR
    # ==============================
    @staticmethod
    def aprobar_solicitud(db: Session, id_solicitud: int):

        solicitud = db.query(ColaboradorMes).filter(
            ColaboradorMes.id == id_solicitud
        ).first()

        if not solicitud:
            return None

        # ==============================
        # VALIDACIÓN CENTRALIZADA
        # ==============================
        ya_existe = ColaboradorMesRepository.existe_asignacion_mes(
            db,
            solicitud.departamento,
            solicitud.mes,
            solicitud.anio
        )

        if ya_existe:
            raise Exception("Ya existe un colaborador del mes para este periodo")

        # ==============================
        # ACTUALIZAR ESTADO
        # ==============================
        solicitud.estado = "ACEPTADO"
        solicitud.fecha_asignacion = datetime.now()

        try:
            db.commit()
            db.refresh(solicitud)

            colaborador = db.query(Colaborador).filter(
                Colaborador.numero_nomina == solicitud.numero_nomina
            ).first()

            return {
                "id": solicitud.id,
                "numero_nomina": solicitud.numero_nomina,
                "nombre": colaborador.nombre if colaborador else None,
                "puesto_real": colaborador.puesto if colaborador else None,
                "departamento": solicitud.departamento,
                "motivo_solicitud": solicitud.motivo_solicitud,
                "mes": solicitud.mes,
                "anio": solicitud.anio,
                "estado": solicitud.estado,
                "fecha_solicitud": solicitud.fecha_solicitud,
                "fecha_asignacion": solicitud.fecha_asignacion
            }

        except Exception as e:
            db.rollback()
            raise e
        
    @staticmethod
    def obtener_actual(
        db: Session,
        departamento: str
    ):
        hoy = datetime.now()

        solicitud = (
            db.query(ColaboradorMes)
            .filter(
                ColaboradorMes.departamento == departamento,
                ColaboradorMes.mes == hoy.month,
                ColaboradorMes.anio == hoy.year,
                ColaboradorMes.estado == "ACEPTADO"
            )
            .first()
        )

        if not solicitud:
            return None

        colaborador = (
            db.query(Colaborador)
            .filter(
                Colaborador.numero_nomina == solicitud.numero_nomina
            )
            .first()
        )

        return {
            "id": solicitud.id,
            "numero_nomina": solicitud.numero_nomina,
            "nombre": colaborador.nombre if colaborador else None,
            "puesto_real": colaborador.puesto if colaborador else None,
            "departamento": solicitud.departamento,
            "motivo_solicitud": solicitud.motivo_solicitud,
            "mes": solicitud.mes,
            "anio": solicitud.anio,
            "estado": solicitud.estado,
            "fecha_solicitud": solicitud.fecha_solicitud,
            "fecha_asignacion": solicitud.fecha_asignacion
        }
    
    @staticmethod
    def solicitud_activa_departamento(
        db: Session,
        departamento: str
    ):
        hoy = datetime.now()

        return (
            db.query(ColaboradorMes)
            .filter(
                ColaboradorMes.departamento == departamento,
                ColaboradorMes.estado.in_(["PENDIENTE", "ACEPTADO"]),
                ColaboradorMes.mes == hoy.month,
                ColaboradorMes.anio == hoy.year
            )
            .first()
            is not None
        )
    
    @staticmethod
    def existe_asignacion_mes(db: Session, departamento: str, mes: int, anio: int):
        return db.query(ColaboradorMes).filter(
            ColaboradorMes.departamento == departamento,
            ColaboradorMes.mes == mes,
            ColaboradorMes.anio == anio,
            ColaboradorMes.estado == "ACEPTADO"
        ).first() is not None
    
    @staticmethod
    def obtener_historial(
        db: Session,
        departamento: str
    ):
        resultados = (
            db.query(
                ColaboradorMes.numero_nomina,
                Colaborador.nombre,
                ColaboradorMes.departamento,
                ColaboradorMes.puesto,
                ColaboradorMes.mes,
                ColaboradorMes.anio
            )
            .join(
                Colaborador,
                Colaborador.numero_nomina == ColaboradorMes.numero_nomina
            )
            .filter(
                ColaboradorMes.departamento == departamento,
                ColaboradorMes.estado == "ACEPTADO"
            )
            .order_by(
                ColaboradorMes.anio.desc(),
                ColaboradorMes.mes.desc()
            )
            .all()
        )
        return [
            {
                "numero_nomina": item.numero_nomina,
                "nombre": item.nombre,
                "departamento": item.departamento,
                "puesto": item.puesto,
                "mes": item.mes,
                "anio": item.anio
            }
            for item in resultados
        ]