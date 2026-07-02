from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from datetime import datetime, date
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
        
        # Solo las solicitudes pendientes pueden procesarse
        if solicitud.estado != "PENDIENTE":
            raise HTTPException(
                status_code=400,
                detail="La solicitud ya fue procesada"
            )

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
            raise HTTPException(
                status_code=400,
                detail="Ya existe un colaborador del mes para este periodo"
            )

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
                "area": solicitud.area,
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
    
    # ==============================
    # RECHAZAR SOLICITUD
    # ==============================
    @staticmethod
    def rechazar_solicitud(db: Session, id_solicitud: int):

        solicitud = db.query(ColaboradorMes).filter(
            ColaboradorMes.id == id_solicitud
        ).first()

        if not solicitud:
            return None
        
        # Solo las solicitudes pendientes pueden procesarse
        if solicitud.estado != "PENDIENTE":
            raise HTTPException(
                status_code=400,
                detail="La solicitud ya fue procesada"
            )

        solicitud.estado = "RECHAZADO"

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
                "area": solicitud.area,
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
            "area": solicitud.area,
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
        departamento: str,
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
                ColaboradorMes.area,
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
                "area": item.area,
                "puesto": item.puesto,
                "mes": item.mes,
                "anio": item.anio
            }
            for item in resultados
        ]
    
    # ==============================
    # HISTORIAL ADMIN 
    # ==============================
    @staticmethod
    def obtener_historial_admin(
        db: Session,
        id: int | None = None,
        numero_nomina: str | None = None,
        nombre: str | None = None,
        departamento: str | None = None,
        area: str | None = None,
        fecha_solicitud: date | None = None,
        estado: str | None = None,
        offset: int = 0,
        limit: int = 10
    ):

        query = (
            db.query(
                ColaboradorMes.id,
                ColaboradorMes.numero_nomina,
                Colaborador.nombre,
                ColaboradorMes.departamento,
                ColaboradorMes.area,
                ColaboradorMes.puesto,
                ColaboradorMes.mes,
                ColaboradorMes.anio,
                ColaboradorMes.fecha_solicitud,
                ColaboradorMes.estado
            )
            .join(
                Colaborador,
                Colaborador.numero_nomina == ColaboradorMes.numero_nomina
            )
            .order_by(
                ColaboradorMes.fecha_solicitud.desc()
            )
        )

        if id:
            query = query.filter(ColaboradorMes.id == id)

        if numero_nomina:
            query = query.filter(ColaboradorMes.numero_nomina == numero_nomina)

        if nombre:
            query = query.filter(Colaborador.nombre == nombre)

        if departamento:
            query = query.filter(ColaboradorMes.departamento == departamento)
        
        if area:
            query = query.filter(
                ColaboradorMes.area == area
            )

        if fecha_solicitud:
            query = query.filter(
                cast(ColaboradorMes.fecha_solicitud, Date) == fecha_solicitud
            )

        if estado:
            query = query.filter(ColaboradorMes.estado == estado)

        total = query.count()

        resultados = (
            query
            .order_by(
                ColaboradorMes.anio.desc(),
                ColaboradorMes.mes.desc()
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "total": total,
            "data": [
                {
                    "id": item.id,
                    "numero_nomina": item.numero_nomina,
                    "nombre": item.nombre,
                    "departamento": item.departamento,
                    "area": item.area,
                    "puesto": item.puesto,
                    "mes": item.mes,
                    "anio": item.anio,
                    "fecha_solicitud": item.fecha_solicitud,
                    "estado": item.estado
                }
                for item in resultados
            ]
        }
    
    @staticmethod
    def contar_asignados(db: Session):

        return (
            db.query(ColaboradorMes)
            .filter(ColaboradorMes.estado == "ACEPTADO")
            .count()
        )
    
    @staticmethod
    def contar_pendientes(db: Session):

        return (
            db.query(ColaboradorMes)
            .filter(ColaboradorMes.estado == "PENDIENTE")
            .count()
        )
    
    @staticmethod
    def obtener_por_id(db: Session, id_solicitud: int):
        query = (
            db.query(
                ColaboradorMes.id,
                ColaboradorMes.numero_nomina,
                Colaborador.nombre,
                ColaboradorMes.departamento,
                ColaboradorMes.area,
                ColaboradorMes.puesto,
                ColaboradorMes.mes,
                ColaboradorMes.anio,
                ColaboradorMes.motivo_solicitud,
                ColaboradorMes.fecha_solicitud,
                ColaboradorMes.estado
            )
            .join(
                Colaborador,
                Colaborador.numero_nomina == ColaboradorMes.numero_nomina
            )
            .filter(ColaboradorMes.id == id_solicitud)
            .first()
        )

        if not query:
            return None
         
        return {    
            "id": query.id,
            "numero_nomina": query.numero_nomina,
            "nombre": query.nombre,
            "departamento": query.departamento,
            "area": query.area,
            "puesto": query.puesto,
            "mes": query.mes,
            "anio": query.anio,
            "motivo_solicitud": query.motivo_solicitud,
            "fecha_solicitud": query.fecha_solicitud,
            "estado": query.estado
        }