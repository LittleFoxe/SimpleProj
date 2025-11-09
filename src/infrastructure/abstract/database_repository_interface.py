from abc import ABC, abstractmethod
from typing import List
from domain.incident import Incident

class IDatabaseRepository(ABC):
    """
    Интерфейс репозитория для работы с базой данных.
    
    Определяет контракт для работы с данными инцидентов в БД.
    Может быть расширен дополнительными методами для работы с инцидентами.
    """
    
    @abstractmethod
    def create_incident(self, incident: Incident) -> None:
        """
        Создает новый инцидент в базе данных.
        
        Args:
            incident: Доменный объект инцидента
        """
        pass

    @abstractmethod
    def get_incidents_by_status(self, status: str) -> List[Incident]:
        """
        Возвращает список инцидентов с указанным статусом.
        
        Args:
            status: Статус инцидентов для фильтрации
            
        Returns:
            List[Incident]: Список доменных объектов инцидентов
        """
        pass

    @abstractmethod
    def update_incident_status(self, id: int, new_status: str) -> None:
        """
        Обновляет статус инцидента по его идентификатору.
        
        Args:
            id: Идентификатор инцидента
            new_status: Новый статус инцидента
        """
        pass
    
    # Данный интерфейс потом может расширять функционал для других сервисов,
    # если возникнет необходимость в новых таблицах помимо Incident
    