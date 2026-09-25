from fastapi import APIRouter

router = APIRouter(prefix="/aprendices", tags=["Gestión de Aprendices"])

@router.get("/")
def obtener_aprendices():
    return {"mensaje": "Lista de aprendices"}