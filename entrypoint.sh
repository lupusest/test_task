#!/bin/sh

# Ожидаем, пока база данных будет готова
# В реальном проекте здесь лучше использовать более надежный скрипт,
# например, wait-for-it.sh, но для тестового задания sleep достаточно.
echo "Waiting for database..."
sleep 5

# Применяем миграции базы данных
echo "Applying database migrations..."
python manage.py migrate

# Собираем статические файлы
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Запускаем команду для наполнения базы данными и создания админа
echo "Seeding data..."
python manage.py seed_data

# Запускаем Gunicorn сервер
echo "Starting Gunicorn..."
exec gunicorn test_task.wsgi:application --bind 0.0.0.0:8000
