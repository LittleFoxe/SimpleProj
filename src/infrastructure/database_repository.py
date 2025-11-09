from typing import List
from sqlalchemy.orm import Session
from domain.incident import Incident
from infrastructure.abstract.database_repository_interface import IDatabaseRepository

class DatabaseRepository(IDatabaseRepository):
    def __init__(self, session: Session):
        """
        Инициализирует репозиторий для работы с базой данных.
        
        Args:
            session: Сессия SQLAlchemy для работы с базой данных
        """
        self.session = session

    def create_incident(self, incident: Incident) -> None:
        """
        Создает новый инцидент в базе данных.
        
        Args:
            incident: Доменный объект инцидента
        """
        self.session.add(incident)
        self.session.commit()

    def get_incidents_by_status(self, status: str) -> List[Incident]:
        """
        Возвращает список инцидентов с указанным статусом.
        
        Args:
            status: Статус инцидентов для фильтрации
            
        Returns:
            List[Incident]: Список доменных объектов инцидентов
        """
        return self.session.query(Incident).filter(Incident.status == status).all()

    def update_incident_status(self, id: int, new_status: str) -> None:
        """
        Обновляет статус инцидента по его идентификатору.
        
        Args:
            id: Идентификатор инцидента
            new_status: Новый статус инцидента
        """
        incident = self.session.query(Incident).filter(Incident.id == id).first()
        
        if not incident:
            raise ValueError(f"Инцидент с id {id} не найден")
        
        incident.status = new_status
        self.session.commit()