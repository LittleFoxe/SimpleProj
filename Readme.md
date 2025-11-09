# Приложение для сохранения инцидентов

## Запуск приложения
1. Активация виртуального окружения
```bash
# Для Windows:
.venv\Scripts\activate
# Для Linux/MacOS:
source venv/bin/activate
```
2. Установка зависимостей
```bash
pip install -r requirements.txt
```
3. Запуск приложения
```bash
python src/main.py
```

После запуска приложения документация доступна по адресам:\
**Swagger UI**: http://localhost:8000/docs\
**ReDoc**: http://localhost:8000/redoc

## Основные эндпоинты
1. **POST**: http://localhost:8000/incidents/

**Пример использования**
```bash
curl -X POST "http://localhost:8000/incidents/" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Самокат не в сети",
       "status": "pending",
       "source": "monitoring"
     }'
```

2. **GET**: http://localhost:8000/incidents/?status={название_статуса}

**Пример использования**
```bash
curl -X GET "http://localhost:8000/incidents/?status=pending"
```

3. **PATCH**: http://localhost:8000/incidents/{ID_инцидента}/status

**Пример использования**
```bash
curl -X PATCH "http://localhost:8000/incidents/1/status" \
     -H "Content-Type: application/json" \
     -d '{"new_status": "in progress"}'
```

## Вспомогательные эндпоинты
1. **GET**: http://localhost:8000/ \
Точка входа по умолчанию, выводящая название текущего микросервиса:
```json
{
  "message": "Incident Management System API"
}
```

2. **GET**: http://localhost:8000/health \
Эндпоинт для проверки состояния микросервиса. Отправляет пустой ответ со статусом 200.