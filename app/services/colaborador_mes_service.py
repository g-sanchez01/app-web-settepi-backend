from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models.colaborador_mes import ColaboradorMes
from app.models.colaborador import Colaborador
from app.repositories.colaborador_mes_repository import ColaboradorMesRepository


def crear_solicitud(db: Session, data, user):

    # ==============================
    # 1. VALIDACIONES BÁSICAS
    # ==============================
    if not data.numero_nomina:
        raise HTTPException(400, "Número de nómina requerido")

    if not data.departamento:
        raise HTTPException(400, "Departamento requerido")

    if not data.puesto:
        raise HTTPException(400, "Puesto requerido")

    if not data.motivo_solicitud:
        raise HTTPException(400, "El motivo de la solicitud es obligatorio")

    now = datetime.now()

    # ==============================
    # 2. VALIDACIÓN 1: DUPLICADO MES + AÑO
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
    # 3. VALIDACIÓN 2: SOLICITUD PENDIENTE
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
    # 4. CONSTRUCCIÓN DEL MODELO
    # ==============================
    nueva_solicitud = ColaboradorMes(
        numero_nomina=data.numero_nomina,
        departamento=data.departamento,
        puesto=data.puesto,
        motivo_solicitud=data.motivo_solicitud,

        mes=now.month,
        anio=now.year,

        fecha_solicitud=now,
        estado="PENDIENTE"
    )

    # ==============================
    # 5. GUARDADO EN REPOSITORY
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
    if user.rol != "ADMIN":
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