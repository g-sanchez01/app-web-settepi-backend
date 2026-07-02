from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, date

from app.models.colaborador_mes import ColaboradorMes
from app.models.colaborador import Colaborador
from app.repositories.colaborador_mes_repository import ColaboradorMesRepository


def crear_solicitud(db: Session, data, user):

    now = datetime.now()

    # ==============================
    # 1. VALIDACIONES BÁSICAS
    # ==============================
    if not data.numero_nomina:
        raise HTTPException(400, "Número de nómina requerido")

    if not data.motivo_solicitud:
        raise HTTPException(400, "El motivo de la solicitud es obligatorio")
    
    # ==============================
    # 2. OBTENER COLABORADOR
    # ==============================
    colaborador = db.query(Colaborador).filter(
        Colaborador.numero_nomina == data.numero_nomina
    ).first()

    if not colaborador:
        raise HTTPException(
            status_code=404,
            detail="Colaborador no encontrado"
        )
    
    # ==============================
    # 3. VALIDACIÓN: DUPLICADO MES + AÑO
    # ==============================
    duplicado_mes = db.query(ColaboradorMes).filter(
        ColaboradorMes.numero_nomina == data.numero_nomina,
        ColaboradorMes.mes == now.month,
        ColaboradorMes.anio == now.year
    ).first()

    if duplicado_mes:
        raise HTTPException(
            status_code=400,
            detail="Este colaborador ya fue registrado en este mes"
        )
    
    # ==============================
    # 4. VALIDACIÓN : SOLICITUD PENDIENTE
    # ==============================
    solicitud_pendiente = db.query(ColaboradorMes).filter(
        ColaboradorMes.numero_nomina == data.numero_nomina,
        ColaboradorMes.estado == "PENDIENTE"
    ).first()

    if solicitud_pendiente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una solicitud pendiente para este colaborador"
        )
    
    # ==============================
    # 5. VALIDACIÓN: DEPARTAMENTO YA TIENE UNA SOLICITUD ACTIVA
    # ==============================
    solicitud_activa = (
        ColaboradorMesRepository.solicitud_activa_departamento(
            db,
            colaborador.departamento
        )
    )

    if solicitud_activa:
        raise HTTPException(
            status_code=400,
            detail=(
                "Ya existe una solicitud pendiente o aprobada "
                "para este departamento en el mes actual"
            )
        )

    # ==============================
    # 6. CONSTRUCCIÓN DEL MODELO
    # ==============================
    nueva_solicitud = ColaboradorMes(
        numero_nomina=colaborador.numero_nomina,
        departamento=colaborador.departamento,
        area=colaborador.area,
        puesto=colaborador.puesto,
        motivo_solicitud=data.motivo_solicitud,

        mes=now.month,
        anio=now.year,

        fecha_solicitud=now,
        estado="PENDIENTE"
    )

    # ==============================
    # 7. GUARDADO EN REPOSITORY
    # ==============================
    try:
        return ColaboradorMesRepository.crear_solicitud(
            db,
            nueva_solicitud
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear solicitud: {str(e)}"
        )
    

def aprobar_solicitud(db: Session, id_solicitud: int, user: Colaborador):

    # VALIDACIÓN DE ROL
    if user.rol not in ["ADMIN", "ADMIN_DEV"]:
        raise HTTPException(
            status_code=403,
            detail="No tienes permisos para aprobar esta solicitud"
        )

    resultado = ColaboradorMesRepository.aprobar_solicitud(db, id_solicitud)

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="Solicitud no encontrada"
        )

    return {
        "message": "Empleado asignado correctamente",
        "data": resultado
    }

def rechazar_solicitud(db: Session, id_solicitud: int, user: Colaborador):

    # VALIDACIÓN DE ROL
    if user.rol not in ["ADMIN", "ADMIN_DEV"]:
        raise HTTPException(
            status_code=403,
            detail="No tienes permisos para aprobar esta solicitud"
        )

    resultado = ColaboradorMesRepository.rechazar_solicitud(db, id_solicitud)

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="Solicitud no encontrada"
        )

    return {
        "message": "Empleado asignado correctamente",
        "data": resultado
    }

def obtener_actual_mes(
    db: Session,
    departamento: str
):
    return ColaboradorMesRepository.obtener_actual(
        db,
        departamento
    )

def obtener_historial_colaborador_mes(
    db: Session,
    user: Colaborador
):
    return ColaboradorMesRepository.obtener_historial(
        db=db,
        departamento=user.departamento
    )

def obtener_historial_admin(
    db: Session,
    user: Colaborador,
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

    if user.rol not in ["ADMIN", "ADMIN_DEV"]:
        raise HTTPException(
            status_code=403,
            detail="No tienes permisos para ver esta información"
        )

    return ColaboradorMesRepository.obtener_historial_admin(
        db=db,
        id=id,
        numero_nomina=numero_nomina,
        nombre=nombre,
        departamento=departamento,
        area=area,
        fecha_solicitud=fecha_solicitud,
        estado=estado,
        offset=offset,
        limit=limit
    )

def contar_asignados(db: Session):
    return ColaboradorMesRepository.contar_asignados(db)

def contar_pendientes(db: Session):
    return ColaboradorMesRepository.contar_pendientes(db)