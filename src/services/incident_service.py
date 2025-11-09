from typing import List
from services.dto.incident_dto import IncidentDTO, IncidentStatus
from services.abstract.incident_interface import IIncidentService
from domain.incident import Incident
from infrastructure.abstract.database_repository_interface import IDatabaseRepository


class IncidentService(IIncidentService):
    def __init__(self, repository: IDatabaseRepository):
        """
        Инициализирует сервис инцидентов.
        
        Args:
            repository: Репозиторий для работы с базой данных
        """
        self.repository = repository

    def create_incident(self, incident: IncidentDTO) -> None:
        """
        Создает новый инцидент в базе данных из DTO.
        
        Args:
            incident_dto: DTO объект с данными инцидента
        """
        # Преобразование DTO в доменную модель для репозитория
        new_incident = Incident(
            text=incident.text,
            status=incident.status,
            source=incident.source,
            created_at=incident.created_at
        )
        
        self.repository.create_incident(new_incident)

    def get_incidents(self, status: str) -> List[IncidentDTO]:
        """
        Возвращает список инцидентов с указанным статусом.
        
        Args:
            status: Статус инцидентов для фильтрации
            
        Returns:
            List[IncidentDTO]: Список DTO объектов инцидентов
            
        Raises:
            ValueError: Если передан недопустимый статус
        """
        # Валидация статуса
        try:
            IncidentStatus(status)
        except ValueError:
            raise ValueError(f"Недопустимый статус: {status}")

        # Получение доменных моделей из репозитория
        incidents = self.repository.get_incidents_by_status(status)
        
        # Преобразование доменных моделей в DTO
        incident_dtos = []
        for incident in incidents:
            incident_dto = IncidentDTO(
                id=incident.id,
                text=incident.text,
                status=incident.status,
                source=incident.source,
                created_at=incident.created_at
            )
            incident_dtos.append(incident_dto)
            
        return incident_dtos

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
                
        Raises:
            ValueError: Если передан недопустимый статус
        """
        # Валидация нового статуса
        try:
            validated_status = IncidentStatus(new_status).value
        except ValueError:
            raise ValueError(f"Недопустимый статус: {new_status}")
        
        # Делегирование операции репозиторию
        try:
            self.repository.update_incident_status(id, validated_status)
        except ValueError:
            return 2

        return 0