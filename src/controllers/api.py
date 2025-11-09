from fastapi import APIRouter, Depends, HTTPException, status as fapi_status, Path
from typing import List, Optional

from services.abstract.incident_interface import IIncidentService
from services.dto.incident_dto import IncidentDTO
from infrastructure.dependency_provider import get_incident_service

router = APIRouter(prefix="/incidents", tags=["incidents"])

# Pydantic модели для запросов и ответов
from pydantic import BaseModel, Field

class IncidentCreateRequest(BaseModel):
    """
    Модель запроса для создания нового инцидента.
    
    Attributes:
        text: Текст описания инцидента
        status: Статус инцидента (по умолчанию "pending")
        source: Источник инцидента
    """
    text: str = Field(..., example="Самокат не в сети", description="Текст описания инцидента")
    status: Optional[str] = Field(default="pending", example="pending", description="Статус инцидента")
    source: str = Field(..., example="monitoring", description="Источник инцидента")

    class Config:
        schema_extra = {
            "example": {
                "text": "Самокат не в сети",
                "status": "pending",
                "source": "monitoring"
            }
        }

class IncidentUpdateStatusRequest(BaseModel):
    """
    Модель запроса для обновления статуса инцидента.
    
    Attributes:
        new_status: Новый статус инцидента
    """
    new_status: str = Field(..., example="in progress", description="Новый статус инцидента")

class IncidentResponse(BaseModel):
    """
    Модель ответа с данными инцидента.
    
    Attributes:
        id: Уникальный идентификатор инцидента
        text: Текст описания инцидента
        status: Текущий статус инцидента
        source: Источник инцидента
        created_at: Дата и время создания инцидента
    """
    id: Optional[int] = Field(None, example=1, description="Уникальный идентификатор инцидента")
    text: str = Field(..., example="Самокат не в сети", description="Текст описания инцидента")
    status: str = Field(..., example="pending", description="Текущий статус инцидента")
    source: str = Field(..., example="monitoring", description="Источник инцидента")
    created_at: Optional[str] = Field(None, example="2023-10-01T12:00:00Z", description="Дата и время создания инцидента")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "text": "Самокат не в сети",
                "status": "pending",
                "source": "monitoring",
                "created_at": "2023-10-01T12:00:00Z"
            }
        }


@router.post(
    "/", 
    status_code=fapi_status.HTTP_201_CREATED,
    summary="Создать новый инцидент",
    response_description="Сообщение о успешном создании инцидента",
    responses={
        201: {
            "description": "Инцидент успешно создан",
            "content": {
                "application/json": {
                    "example": {"message": "Новый инцидент добавлен в базу данных!"}
                }
            }
        },
        400: {
            "description": "Неверные данные запроса",
            "content": {
                "application/json": {
                    "example": {"detail": "Недопустимый статус: 'invalid_status'. Допустимые значения: pending, solved, in progress"}
                }
            }
        },
        500: {
            "description": "Внутренняя ошибка сервера",
            "content": {
                "application/json": {
                    "example": {"detail": "Ошибка при создании инцидента: ..."}
                }
            }
        }
    }
)
async def create_incident(
    incident_data: IncidentCreateRequest,
    service: IIncidentService = Depends(get_incident_service)
):
    """
    Создает новый инцидент в системе.
    
    Этот endpoint позволяет добавить новый инцидент в базу данных с указанием
    текста описания, статуса и источника инцидента.
    """
    try:
        # Создаем DTO из запроса
        incident_dto = IncidentDTO(
            text=incident_data.text,
            status=incident_data.status,
            source=incident_data.source
        )
        
        # Создаем инцидент через сервис
        service.create_incident(incident_dto)
        
        # Если всё в порядке - выводим сообщение об успешном создании
        return {"message": "Новый инцидент добавлен в базу данных!"}
        
    except ValueError as e:
        raise HTTPException(
            status_code=fapi_status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=fapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании инцидента: {str(e)}"
        )


@router.get(
    "/", 
    response_model=List[IncidentResponse],
    summary="Получить список инцидентов",
    response_description="Список инцидентов с указанным статусом",
    responses={
        200: {
            "description": "Список инцидентов успешно получен",
            "content": {
                "application/json": {
                    "examples": {
                        "pending": {
                            "summary": "Инциденты со статусом pending",
                            "value": [
                                {
                                    "id": 1,
                                    "text": "Самокат не в сети",
                                    "status": "pending",
                                    "source": "monitoring",
                                    "created_at": "2023-10-01T12:00:00Z"
                                }
                            ]
                        },
                        "solved": {
                            "summary": "Инциденты со статусом solved",
                            "value": [
                                {
                                    "id": 2,
                                    "text": "Проблема с платежной системой",
                                    "status": "solved",
                                    "source": "operator",
                                    "created_at": "2023-10-01T10:00:00Z"
                                }
                            ]
                        }
                    }
                }
            }
        },
        400: {
            "description": "Неверный статус для фильтрации",
            "content": {
                "application/json": {
                    "example": {"detail": "Недопустимый статус: 'invalid_status'"}
                }
            }
        },
        500: {
            "description": "Внутренняя ошибка сервера",
            "content": {
                "application/json": {
                    "example": {"detail": "Ошибка при получении инцидентов: ..."}
                }
            }
        }
    }
)
async def get_incidents(
    status: Optional[str] = None,
    service: IIncidentService = Depends(get_incident_service)
):
    """
    Возвращает список инцидентов с возможностью фильтрации по статусу.
    
    Если параметр status не указан, возвращаются инциденты со статусом "pending".
    Допустимые значения статуса: "pending", "in progress", "solved".
    """
    try:
        if status is None:
            # Если статус не указан, можно вернуть все инциденты
            # Для простоты возвращаем pending инциденты
            status = "pending"
        
        incidents = service.get_incidents(status)
        
        # Преобразуем DTO в Pydantic модели для ответа
        incident_responses = []
        for incident in incidents:
            incident_responses.append(IncidentResponse(
                id=incident.id,
                text=incident.text,
                status=incident.status,
                source=incident.source,
                created_at=incident.created_at.isoformat() if incident.created_at else None
            ))
            
        return incident_responses
        
    except ValueError as e:
        raise HTTPException(
            status_code=fapi_status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=fapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении инцидентов: {str(e)}"
        )


@router.patch(
    "/{incident_id}/status", 
    status_code=fapi_status.HTTP_200_OK,
    summary="Обновить статус инцидента",
    response_description="Сообщение о результате обновления статуса",
    responses={
        200: {
            "description": "Статус инцидента успешно обновлен",
            "content": {
                "application/json": {
                    "example": {"message": "Статус инцидента успешно обновлен"}
                }
            }
        },
        400: {
            "description": "Неверный статус или данные запроса",
            "content": {
                "application/json": {
                    "example": {"detail": "Недопустимый статус: 'invalid_status'"}
                }
            }
        },
        404: {
            "description": "Инцидент не найден",
            "content": {
                "application/json": {
                    "example": {"detail": "Инцидент с ID 999 не найден"}
                }
            }
        },
        500: {
            "description": "Внутренняя ошибка сервера",
            "content": {
                "application/json": {
                    "example": {"detail": "Ошибка при обновлении статуса: ..."}
                }
            }
        }
    }
)
async def update_incident_status(
    incident_id: int = Path(..., description="ID инцидента для обновления", example=1),
    status_data: IncidentUpdateStatusRequest = ...,
    service: IIncidentService = Depends(get_incident_service)
):
    """
    Обновляет статус инцидента по его идентификатору.
    
    Позволяет изменить статус существующего инцидента. Допустимые значения статуса:
    "pending", "in progress", "solved".
    """
    try:
        result = service.update_status(incident_id, status_data.new_status)
        
        if result == 0:
            return {"message": "Статус инцидента успешно обновлен"}
        elif result == 2:
            raise HTTPException(
                status_code=fapi_status.HTTP_404_NOT_FOUND,
                detail=f"Инцидент с ID {incident_id} не найден"
            )
        else:
            raise HTTPException(
                status_code=fapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Неизвестная ошибка при обновлении статуса"
            )
            
    except ValueError as e:
        raise HTTPException(
            status_code=fapi_status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=fapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении статуса: {str(e)}"
        )
