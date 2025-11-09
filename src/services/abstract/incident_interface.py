from abc import ABC, abstractmethod
from typing import List

from services.dto.incident_dto import IncidentDTO

class IIncidentService(ABC):
    
    @abstractmethod
    def create_incident(self, incident: IncidentDTO) -> None:
        """
        Создает новый инцидент на основе данных из DTO.
        
        Args:
            incident: DTO объект с данными инцидента
        """
        pass

    @abstractmethod
    def get_incidents(self, status: str) -> List[IncidentDTO]:
        """
        Возвращает список инцидентов с указанным статусом.
        
        Args:
            status: Статус инцидентов для фильтрации
            
        Returns:
            List[IncidentDTO]: Список DTO объектов инцидентов
        """
        pass

    @abstractmethod
    def update_status(self, id: int, new_status: str) -> int:
        """
        Обновляет статус инцидента по его идентификатору.
        
        Args:
            id: Идентификатор инцидента
            new_status: Новый статус инцидента
            
        Returns:
            int: Код результата операции:
                0 - операция выполнена успешно
                2 - инцидент с указанным id не найден
        """
        pass