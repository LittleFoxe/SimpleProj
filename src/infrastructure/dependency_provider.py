from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from infrastructure.database_repository import DatabaseRepository
from services.abstract.incident_interface import IIncidentService
from services.incident_service import IncidentService

"""Набор методов для реализации внедрения зависимостей по всему приложению"""

def _get_database_engine():
    """
    Создает и возвращает движок SQLAlchemy для работы с базой данных.
    
    Returns:
        Engine: Объект движка SQLAlchemy
    """
    return create_engine('sqlite:///incidents.db', echo=True)

@contextmanager
def get_database_session():
    """
    Контекстный менеджер для безопасной работы с сессией БД.
    
    Yields:
        Session: Объект сессии SQLAlchemy
    """
    engine = _get_database_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def get_incident_service() -> IIncidentService:
    """
    Реализация DI для сервиса инцидентов, определяющая тип БД репозитория данного сервиса.

    Важно: создает сервис с сессией, которая будет закрыта после использования.
    Для использования в FastAPI Depends это нормально, так как каждый запрос
    получает свою сессию.
    
    Returns:
        IIncidentService: Сервис для работы с инцидентами
    """
    with get_database_session() as session:
        repository = DatabaseRepository(session=session)
        service = IncidentService(repository=repository)
        return service

# Альтернативная версия для использования в тестах или других контекстах
@contextmanager
def incident_service_context() -> IIncidentService:
    """
    Контекстный менеджер для работы с сервисом инцидентов.
    
    Yields:
        IIncidentService: Сервис для работы с инцидентами
    """
    with get_database_session() as session:
        repository = DatabaseRepository(session=session)
        service = IncidentService(repository=repository)
        yield service