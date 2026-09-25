from fastapi import FastAPI
import models
from database import engine

from routers import compras, auth, aprendices

# Creación de tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Sistema ADSO")

# Registro de routers
app.include_router(auth.router)
app.include_router(aprendices.router)
app.include_router(compras.router)