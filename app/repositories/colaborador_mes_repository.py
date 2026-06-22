from sqlalchemy.orm import Session
from datetime import datetime

from app.models.colaborador_mes import ColaboradorMes
from app.models.colaborador import Colaborador


class ColaboradorMesRepository:

    @staticmethod
    def crear_solicitud(db: Session, data: ColaboradorMes):

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
        # VALIDACIÓN: YA EXISTE APROBADO
        # ==============================
        existing = db.query(ColaboradorMes).filter(
            ColaboradorMes.departamento == solicitud.departamento,
            ColaboradorMes.mes == solicitud.mes,
            ColaboradorMes.anio == solicitud.anio,
            ColaboradorMes.estado == "ACEPTADO"
        ).first()

        if existing:
            raise Exception("Ya existe un colaborador del mes aprobado")

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