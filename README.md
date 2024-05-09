Ботоферма
==============
***Содержание:***
- [Чек-лист](#Check-list)
- [Запуск контейнеров](#Run-container)
- [Дополнительные команды](#Addition)


# Чек-лист <a name="Check-list"></a>
 - [x] Наложение и снятие блокировки на/с пользователя
 - [x] Механизм авторизации OAuth2
 - [x] Валидация входных данных посредством Pydantic
 - [x] Переменные окружения считываются из .env файла посредством Pydantic
 - [x] Использование линтера (flake8), pytetst
 - [x] Наличие docs-strings и type-hints
 - [x] Разворачивается с помощью docker-compose
 - [x] Использование Dependency Injection
 - [x] Сервис написан в асинхронном стиле
 - [x] Используется Alembic для миграций




# Запуск контейнеров <a name="Run-container"></a>

### Первый запуск:

```bash
docker-compose up -d --build
```
```bash
docker compose exec app migrate
```

### Перейдите по странице:
```html
http://0.0.0.0:8000/docs
```

# Дополнительные команды <a name="Addition"></a>
1. Проверка линтером
```bash
flake8 src
```
2. Тесты и покрытие
```bash
pytest
```
```bash
pytest --cov=src tests
```