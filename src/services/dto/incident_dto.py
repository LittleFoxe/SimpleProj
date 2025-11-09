from datetime import datetime, timezone
from typing import Optional, Union
from enum import Enum

class IncidentStatus(str, Enum):
    PENDING = "pending"
    SOLVED = "solved"
    IN_PROGRESS = "in progress"

class IncidentSource(str, Enum):
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"

class IncidentDTO:
    """DTO для сущности Incident"""
    
    def __init__(
        self,
        text: str,
        status: Union[IncidentStatus, str],
        source: Union[IncidentSource, str],
        id: Optional[int] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.text = text
        self.status = self._validate_status(status)
        self.source = self._validate_source(source)
        self.created_at = created_at or datetime.now(timezone.utc)

    def _validate_status(self, status: Union[IncidentStatus, str]) -> str:
        """Валидация статуса инцидента"""
        if isinstance(status, IncidentStatus):
            return status.value
        
        status_str = str(status).lower().strip()
        valid_statuses = {item.value for item in IncidentStatus}
        
        if status_str not in valid_statuses:
            raise ValueError(
                f"Недопустимый статус: '{status}'. "
                f"Допустимые значения: {', '.join(valid_statuses)}"
            )
        return status_str

    def _validate_source(self, source: Union[IncidentSource, str]) -> str:
        """Валидация источника инцидента"""
        if isinstance(source, IncidentSource):
            return source.value
        
        source_str = str(source).lower().strip()
        valid_sources = {item.value for item in IncidentSource}
        
        if source_str not in valid_sources:
            raise ValueError(
                f"Недопустимый источник: '{source}'. "
                f"Допустимые значения: {', '.join(valid_sources)}"
            )
        return source_str