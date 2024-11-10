# Система мониторинга образовательной среды ВУЗа

Веб-приложение для отслеживания и управления жалобами по инфраструктуре университета. Система позволяет студентам подавать жалобы, а администраторам и менеджерам - обрабатывать их.

## Функциональность

- Подача жалоб с указанием корпуса и подразделения
- Панель менеджера для обработки жалоб
- Административная панель для полного управления системой
- Система статусов жалоб
- Аутентификация пользователей

## Технологии

- Python 3.8+
- Django 5.1.3
- SQLite
- HTML/CSS
- Font Awesome

## Установка и запуск

1. Клонируйте репозиторий:
git clone https://github.com/your-username/university-monitoring.git
cd university-monitoring

2. Создайте виртуальное окружение и активируйте его:
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows

3. Установите зависимости:
pip install -r requirements.txt

4. Примените миграции:
python manage.py migrate

5. Создайте начальные данные:
python manage.py shell < main/initial_data.py

6. Запустите сервер разработки:
python manage.py runserver

Доступ к системе

Студенты
- URL: http://localhost:8000/
- Не требует авторизации

Менеджеры  
- URL: http://localhost:8000/manager/
- Логин: manager
- Пароль: manager

Администраторы
- URL: http://localhost:8000/admin-panel/
- Логин: admin
- Пароль: admin

