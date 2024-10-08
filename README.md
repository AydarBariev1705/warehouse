# Управление складом

## Описание проекта
Проект представляет собой REST API для управления процессами на складе, разработанный с использованием FastAPI. 
API позволяет управлять товарами, складскими запасами и заказами.

### Функциональность

1. **Управление товарами**:
    - Создание товара (POST `/products`).
    - Получение списка товаров (GET `/products`).
    - Получение информации о товаре по ID (GET `/products/{id}`).
    - Обновление информации о товаре (PUT `/products/{id}`).
    - Удаление товара (DELETE `/products/{id}`).

2. **Управление заказами**:
    - Создание заказа (POST `/orders`).
    - Получение списка заказов (GET `/orders`).
    - Получение информации о заказе по ID (GET `/orders/{id}`).
    - Обновление статуса заказа (PATCH `/orders/{id}/status`).

3. **Бизнес-логика**:
    - Проверка наличия достаточного количества товара при создании заказа.
    - Обновление количества товара на складе при создании заказа (уменьшение доступного количества).
    - Возвращение ошибки при недостаточном количестве товара на складе.

### Технологии
- **FastAPI**: современный веб-фреймворк для создания API на Python.
- **SQLAlchemy 2**: ORM для работы с базой данных.
- **PostgreSQL**: база данных для хранения товаров и заказов.
- **Docker**: контейнеризация приложения для упрощения развертывания.

### Документация: /docs

## Установка и запуск

1. Клонируйте репозиторий

2. Переименуйте .env.template в .env и заполните его 

3. Постройте и запустите Docker-контейнеры:
    ```
    docker-compose up --build
    ```

