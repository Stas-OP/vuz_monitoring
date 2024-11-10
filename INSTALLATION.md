Инструкция по установке системы мониторинга образовательной среды ВУЗа

1. Подготовка к установке:

- Скачайте и установите Python 3.8 или выше:
  * Перейдите на сайт: https://www.python.org/downloads/
  * Скачайте Python для Windows
  * При установке ОБЯЗАТЕЛЬНО поставьте галочку "Add Python to PATH"
  * Нажмите "Install Now"

2. Установка системы:

- Распакуйте архив university_monitoring.zip на диск C:
  * Создайте папку C:\university_system
  * Распакуйте туда содержимое архива
  * Должна получиться структура: C:\university_system\university_monitoring\...

3. Настройка системы:

- Откройте командную строку Windows:
  * Нажмите Win + R
  * Введите cmd
  * Нажмите Enter

- Введите команды по очереди:
  ```
  cd C:\university_system
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  python manage.py migrate
  python manage.py shell < main/initial_data.py
  python manage.py runserver
  ```

4. Доступ к системе:

Для студентов:
- Откройте браузер
- Введите адрес: http://localhost:8000
- Можно сразу подавать жалобы (регистрация не требуется)

Для менеджеров:
- Откройте браузер
- Введите адрес: http://localhost:8000/manager
- Логин: manager
- Пароль: manager

Для администраторов:
- Откройте браузер
- Введите адрес: http://localhost:8000/admin-panel
- Логин: admin
- Пароль: admin

5. Перезапуск системы:

Если нужно закрыть систему:
- Нажмите Ctrl+C в окне командной строки
- Закройте окно

Чтобы запустить снова:
- Откройте командную строку
- Введите команды:
  ```
  cd C:\university_system
  venv\Scripts\activate
  python manage.py runserver
  ```

6. Возможные проблемы:

Если пишет "python не найден":
- Переустановите Python
- Обязательно поставьте галочку "Add Python to PATH" при установке

Если пишет "порт занят":
- Закройте все окна командной строки
- Перезагрузите компьютер
- Повторите запуск

Если не открывается сайт:
- Проверьте что сервер запущен (командная строка открыта)
- Проверьте адрес в браузере (должен быть точно: http://localhost:8000)

7. Настройка системы:

Изменение списка корпусов:
- Откройте файл C:\university_system\main\initial_data.py
- Найдите список buildings
- Добавьте или измените корпуса
- Сохраните файл
- В командной строке выполните:
  python manage.py shell < main/initial_data.py

Изменение отделов:
- В том же файле найдите список departments
- Измените названия отделов
- Сохраните и выполните ту же команду

7. Изменение логинов и паролей:

Чтобы изменить логин/пароль администратора или менеджера:
- Откройте файл C:\university_system\main\views.py в блокноте
- Найдите следующий код (примерно строки 12-30):

  if username == 'manager' and password == 'manager':
      user, created = User.objects.get_or_create(username='manager')
      if created:
          user.set_password('manager')
          ...
  elif username == 'admin' and password == 'admin':
      user, created = User.objects.get_or_create(username='admin')
      if created:
          user.set_password('admin')
          ...

- Измените логин и пароль:
  * Для менеджера: замените оба слова 'manager' на нужный логин/пароль
  * Для администратора: замените оба слова 'admin' на нужный логин/пароль
- Сохраните файл
- Перезапустите сервер:
  * Нажмите Ctrl+C в командной строке
  * Введите: python manage.py runserver

Пример изменения:
Было:
  if username == 'manager' and password == 'manager':
Стало:
  if username == 'mymanager' and password == 'mypassword123':


