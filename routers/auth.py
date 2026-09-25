from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/registro")
def registro():
    return {"mensaje": "Endpoint de registro en construcción"}

@router.post("/login")
def login():
    return {"mensaje": "Endpoint de login en construcción"}