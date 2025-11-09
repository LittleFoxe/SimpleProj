from fastapi import FastAPI, status
from controllers.api import router as incident_router
from contextlib import asynccontextmanager

from infrastructure.dependency_provider import _get_database_engine
from domain.incident import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: инициализация базы данных
    engine = _get_database_engine()
    Base.metadata.create_all(bind=engine)
    print("База данных инициализирована")
    yield
    # Shutdown: очистка ресурсов
    print("Приложение завершает работу")

app = FastAPI(
    title="Incident Management API",
    description="API для управления инцидентами",
    version="1.0.0",
    lifespan=lifespan
)

# Подключаем роутер
app.include_router(incident_router)

@app.get("/")
async def root():
    return {"message": "Incident Management System API"}

@app.get("/health")
async def health_check():
    return status.HTTP_200_OK

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)