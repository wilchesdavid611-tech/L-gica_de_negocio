from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

import models
import shemas
from database import get_db

router = APIRouter(prefix="/compras", tags=["Compras"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def decodificar_token_jwt(token: str):
    return "usuario@correo.com" 

@router.post("/procesar")
def procesar_compra(
    compra: shemas.CompraInput, 
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
):
    email_usuario = decodificar_token_jwt(token) 
    
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    monto_total = compra.precio_unitario * compra.cantidad
    descuento = 0.0

    if compra.cantidad >= 5:
        descuento = 0.12
    elif 3 <= compra.cantidad <= 4:
        descuento = 0.05 

    monto_total_con_descuento = monto_total * (1 - descuento)

    if usuario.saldo_cuenta < monto_total_con_descuento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Saldo insuficiente. Requiere ${monto_total_con_descuento} y su saldo actual es ${usuario.saldo_cuenta}"
        )

    usuario.saldo_cuenta -= monto_total_con_descuento
    db.commit()
    db.refresh(usuario) 

    return {
        "mensaje": "Transacción exitosa",
        "nuevo_saldo": usuario.saldo_cuenta,
        "resumen_compra": {
            "producto": compra.nombre_producto,
            "cantidad_comprada": compra.cantidad,
            "precio_unitario": compra.precio_unitario,
            "subtotal": monto_total,
            "porcentaje_descuento_aplicado": f"{descuento * 100}%",
            "total_cobrado": monto_total_con_descuento
        }
    }