# CCTV Management System

Учебное веб-приложение для управления источниками видеопотока.

## Технологии
- Frontend: Vue 3, Vite, Axios
- Backend: FastAPI, SQLAlchemy
- Database: PostgreSQL 15
- Запуск: Docker Compose

## Запуск через Docker

Требуется установленный и запущенный Docker Desktop (Windows/macOS) или Docker Engine с Compose plugin (Linux).

1. Распакуйте проект.
2. Откройте терминал в корневой папке, где находится `docker-compose.yml`.
3. Выполните:

   ```bash
   docker compose up --build
   ```

4. Откройте:
   - Frontend: http://localhost:5173
   - API и Swagger UI: http://localhost:8000/docs

Для остановки нажмите `Ctrl+C`, затем выполните `docker compose down`.

Данные PostgreSQL хранятся в Docker volume `postgres_data`. Чтобы удалить контейнеры вместе с данными базы, используйте `docker compose down -v` — команда необратимо удалит сохранённые данные.


