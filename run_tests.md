# Инструкция по запуску автоматизированных тестов (Windows)

Эта инструкция показывает, как запустить тесты для информационной системы "Мониторинг ВУЗа".

## Что нужно установить

- Python 3.8 или новее
- Django 3.2 или новее

## Подготовка к запуску

1. Скачайте проект
2. Откройте командную строку Windows (нажмите Win+R, введите cmd и нажмите Enter)
3. Перейдите в папку с проектом:
   ```
   cd путь_к_папке_проекта
   ```

4. Установите необходимые библиотеки:
   ```
   pip install -r requirements.txt
   ```

5. Создайте базу данных для тестов:
   ```
   python manage.py migrate
   ```

## Запуск тестов

### Запуск всех тестов сразу

```
python manage.py test main
```

### Запуск определенной группы тестов

```
python manage.py test main.tests.ModelTests
python manage.py test main.tests.ViewTests
python manage.py test main.tests.SecurityTests
```

### Запуск одного конкретного теста

```
python manage.py test main.tests.ViewTests.test_submit_complaint_creation
```

## Как понять результаты

### Если тесты прошли успешно

Вы увидите сообщение:

```
Ran 15 tests in 2.456s

OK
```

### Если тесты не прошли

Вы увидите сообщение об ошибке:

```
FAIL: test_submit_complaint_validation (main.tests.ViewTests)
----------------------------------------------------------------------
...
AssertionError: ...
```

## Частые проблемы

### Тесты не видят таблицы в базе данных

Решение:
```
python manage.py makemigrations
python manage.py migrate
```

### Проблемы с базой данных

Решение - очистить базу:
```
python manage.py flush --no-input
```