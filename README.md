# Проект на Django

## Установка зависимостей
```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```
 
## Создание и применение миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

## Django Shell Plus
Django Shell Plus - это расширенная интерактивная консоль Django с дополнительными возможностями:

```bash
# Запуск расширенной консоли с автоматическим импортом всех моделей
python manage.py shell_plus

# Запуск с выводом SQL-запросов для отладки
python manage.py shell_plus --print-sql
```

Преимущества shell_plus:
- Автоматический импорт всех моделей проекта
- Автоматический импорт основных модулей Django
- История команд и автодополнение
- Возможность просмотра генерируемых SQL-запросов
- Удобная среда для тестирования кода и работы