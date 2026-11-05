# DBOperations

## Подключение к БД

Конфигурация берётся из переменных окружения (файл `.env`). Шаблон — `.env.example`:

```env
MODE="test"
DBNAME="KitchBot"
DBDBUSER="postgres"
PASSWORD=""
HOST="127.0.0.1"
PORT="5432"
```

Скопируй `.env.example` в `.env` и заполни пароль.

```bash
cp .env.example .env
```

## Установка зависимостей

```bash
python3 -m venv backend/venv
pip install -r backend/DBOperations/requirements.txt
```

## Инициализация базы данных

Таблицы создаются **только** через yoyo-миграции. Скрипт читает SQL-файлы из `migrations/sql/`.

```bash
cd backend/
python3 -m DBOperations.migrations.db_migrations
```

> **Примечание:** в `auth.py` нет `init_db()` — не нужно вызывать ничего вручную. Достаточно запустить миграции один раз.