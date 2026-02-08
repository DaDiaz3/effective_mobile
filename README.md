# Effective Mobile — Backend Test Task

Проект представляет собой backend-сервис на Django с реализацией аутентификации через JWT и авторизации на основе RBAC (Role-Based Access Control). Основная цель — показать понимание принципов безопасности, архитектуры и разделения ответственности между слоями приложения.

1. Используемые технологии

Проект реализован с использованием следующих технологий и инструментов:
- Python 3.10
- Django 5
- Django REST Framework
- PostgreSQL
- JWT (PyJWT)
- Docker / docker-compose
2. Запуск проекта

2.1. Клонирование репозитория
git clone https://github.com/DaDiaz3/effective_mobile.git
cd effective_mobile
2.2. Создание виртуального окружения

python -m venv .venv
.venv\Scripts\activate


2.3. Установка зависимостей

pip install -r requirements.txt


2.4. Переменные окружения

В корне проекта необходимо создать файл .env:

DEBUG=1
SECRET_KEY=django-secret
JWT_SECRET=super-long-secret-key-change-me-1234567890
JWT_ALG=HS256
JWT_TTL_MIN=60


2.5. Применение миграций

python manage.py migrate


2.6. Инициализация RBAC-справочников

python manage.py seed_rbac


2.7. Запуск сервера

python manage.py runserver


3. Аутентификация

Аутентификация реализована с использованием JWT access token.

3.1. Регистрация пользователя

POST /auth/register/


3.2. Логин пользователя

POST /auth/login/


В ответе возвращается access_token, который используется для доступа к защищённым ресурсам.

3.3. Получение текущего пользователя

GET /auth/me/
Authorization: Bearer <token>


4. Авторизация и RBAC

Авторизация реализована через RBAC и вынесена в отдельное приложение.

Используются следующие сущности:

Role — роль пользователя (например, admin, viewer)

BusinessElement — защищаемый бизнес-ресурс (documents и т.д.)

AccessRule — правило доступа (роль + ресурс + действие)

UserRole — связь пользователя с ролью

Принцип работы:

JWT middleware извлекает пользователя из access token

RBACPermission проверяет наличие роли и разрешений

В зависимости от прав возвращается 401 / 403 / 200

5. Пример защищённого ресурса

GET /api/documents/
Authorization: Bearer <token>


Поведение:

без токена — 401 / 403

с токеном, но без роли — 403 Forbidden

с токеном и ролью admin — 200 OK

Пример ответа:
```md
```json
[
  { "id": 1, "title": "Mock Document 1" },
  { "id": 2, "title": "Mock Document 2" }
]


6. Назначение роли пользователю (пример)

python manage.py shell

from apps.accounts.models import User
from apps.rbac.models import Role, UserRole

user = User.objects.get(email="test2@test.com")
admin_role = Role.objects.get(slug="admin")

UserRole.objects.get_or_create(user=user, role=admin_role)


7. Архитектурные решения и допущения

Используется кастомная модель пользователя (apps.accounts.User)

JWT реализован через middleware, без стандартных DRF authentication classes

RBAC вынесен в отдельное приложение

/api/documents/ реализован как mock-ресурс для демонстрации прав доступа

Архитектура позволяет легко добавлять новые роли и бизнес-ресурсы

8. Итог

В рамках проекта реализованы:

JWT аутентификация

middleware-авторизация

RBAC с ролями и правилами доступа

корректная обработка 401 / 403 / 200

Решение демонстрирует понимание принципов backend-разработки и может быть расширено под реальные бизнес-задачи.
