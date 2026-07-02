from sqlalchemy.orm import Session
from datetime import datetime, date
from sqlalchemy import cast, Date, func
from app.models.colaborador import Colaborador
from app.models.colaborador_mes import ColaboradorMes
from app.schemas.usuario import UserCreate

class ColaboradorRepository:

    @staticmethod
    def obtener_por_departamento(
        db: Session,
        departamento: str,
        numero_nomina: str | None = None,
        area: str | None = None,
        offset: int = 0,
        limit: int = 5

    ):
        hoy = datetime.now()

        ultima_solicitud = (
            db.query(
                ColaboradorMes.numero_nomina,
                func.max(ColaboradorMes.id).label("ultimo_id")
            )
            .filter(
                ColaboradorMes.mes == hoy.month,
                ColaboradorMes.anio == hoy.year
            )
            .group_by(ColaboradorMes.numero_nomina)
            .subquery()
        )

        query = (
            db.query(
                Colaborador,
                ColaboradorMes.estado.label("estado_solicitud")
            )
            .outerjoin(
                ultima_solicitud,
                Colaborador.numero_nomina == ultima_solicitud.c.numero_nomina
            )
            .outerjoin(
                ColaboradorMes,
                ColaboradorMes.id == ultima_solicitud.c.ultimo_id
            )
            .filter(
                Colaborador.departamento == departamento,
                Colaborador.estado == "ACTIVO",
                Colaborador.rol != "LIDER",
            )
        )

        if numero_nomina:
            query = query.filter(
                Colaborador.numero_nomina == numero_nomina
            )

        if area:
            query = query.filter(
                Colaborador.area.ilike(f"%{area}%")
            )

        resultados = (
            query
            .order_by(Colaborador.fecha_creacion)
            .offset(offset)
            .limit(limit)
            .all()
        )

        return [
            {
                "numero_nomina": colaborador.numero_nomina,
                "nombre": colaborador.nombre,
                "puesto": colaborador.puesto,
                "departamento": colaborador.departamento,
                "area": colaborador.area,
                "estado_solicitud": estado if estado else "SIN SOLICITUD"
            }
            
            for colaborador, estado in resultados
        ]
    
    @staticmethod
    def contar_integrantes(
        db: Session, 
        departamento: str
    ):
        return (
        db.query(func.count(Colaborador.numero_nomina))
        .filter(
            Colaborador.departamento == departamento,
            Colaborador.estado == "ACTIVO",
            Colaborador.rol != "LIDER"
        )
        .scalar()
    )
    
    # Obtener a todos los usuarios de la plataforma
    @staticmethod
    def obtener_todos(
        db: Session,
        nomina: str | None = None,
        nombre: str | None = None,
        departamento: str | None = None,
        area: str | None = None,
        estado: str | None = None,
        fecha_creacion: date | None = None,
        offset: int = 0,
        limit: int = 10
    ):
        query = db.query(Colaborador)

        if nomina:
            query = query.filter(
                Colaborador.numero_nomina == nomina
            )

        if nombre:
            query = query.filter(
                Colaborador.nombre == nombre
            )
        
        if departamento:
            query = query.filter(
                Colaborador.departamento == departamento
            )

        if area:
            query = query.filter(
                Colaborador.area == area
            )

        if estado:

            if isinstance(estado, list):
                query = query.filter(
                    Colaborador.estado.in_(estado)
                )
            else:
                query = query.filter(
                    Colaborador.estado == estado
                )

        if fecha_creacion:
            query = query.filter(
                cast(Colaborador.fecha_creacion, Date) == fecha_creacion
            )
        
        return (
            query
            .order_by(
                Colaborador.fecha_creacion.desc()
            )
            .offset(offset)
            .limit(limit)
            .all()
        )
    
    # Obtener colaborador por número de nómina
    @staticmethod
    def obtener_por_nomina(
        db: Session,
        numero_nomina: int
    ):
        return (
            db.query(Colaborador)
            .filter(
                Colaborador.numero_nomina == numero_nomina
            )
            .first()
        )
    
    @staticmethod
    def contar_usuarios(db: Session):

        return (
            db.query(Colaborador)
            .filter(Colaborador.estado == "ACTIVO")
            .count()
        )
    
    @staticmethod
    def insertar_usuario(
        db: Session,
        usuario: UserCreate
    ):
        usuario = Colaborador(
            numero_nomina=usuario.numero_nomina,
            nombre=usuario.nombre,
            telefono=usuario.telefono,
            imss=usuario.imss,
            puesto=usuario.puesto,
            departamento=usuario.departamento,
            area=usuario.area,
            estado="ACTIVO",
            rol="GENERAL"
        )

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        return usuario
    
    @staticmethod
    def desactivar_usuario(
        db: Session,
        numero_nomina: int
    ):
        usuario = (
            db.query(Colaborador)
            .filter(
                Colaborador.numero_nomina == numero_nomina
            )
            .first()
        )

        if not usuario:
            return None

        usuario.estado = "BAJA"
        usuario.fecha_actualizacion = datetime.utcnow()

        db.commit()
        db.refresh(usuario)

        return usuario
    
    @staticmethod
    def reactivar_usuario(
        db: Session,
        numero_nomina: int
    ):
        usuario = (
            db.query(Colaborador)
            .filter(
                Colaborador.numero_nomina == numero_nomina
            )
            .first()
        )

        if not usuario:
            return None

        usuario.estado = "ACTIVO"
        usuario.fecha_actualizacion = datetime.utcnow()

        db.commit()
        db.refresh(usuario)

        return usuario

    