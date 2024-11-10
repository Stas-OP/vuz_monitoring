# -*- coding: utf-8 -*-
from main.models import Building, Department, ComplaintStatus

# Создаем корпуса
buildings = [
    {'number': 1, 'name': 'Корпус №1'},
    {'number': 2, 'name': 'Корпус №2'},
    {'number': 3, 'name': 'Корпус №3'},
    {'number': 4, 'name': 'Корпус №4'},
    {'number': 5, 'name': 'Корпус №5'},
    {'number': 6, 'name': 'Корпус №6'},
    {'number': 7, 'name': 'Корпус №7'},
    {'number': 8, 'name': 'Корпус №8'},
    {'number': 9, 'name': 'Корпус №9'},
    {'number': 10, 'name': 'Корпус №10'},
]

# Удаляем старые данные
Building.objects.all().delete()

for building in buildings:
    Building.objects.create(
        number=building['number'],
        name=building['name']
    )

# Создаем подразделения
departments = [
    'Хозяйственная часть',
    'Технический отдел',
    'Администрация ВУЗа'
]

# Удаляем старые данные
Department.objects.all().delete()

for dept in departments:
    Department.objects.create(name=dept)

# Создаем статусы жалоб
statuses = [
    'Новая',  # Начальный статус при создании жалобы
    'Принята в работу',
    'Отложена',
    'Выполнена'
]

# Удаляем старые статусы
ComplaintStatus.objects.all().delete()

# Создаем новые статусы
for status in statuses:
    ComplaintStatus.objects.create(name=status)

print("Начальные данные успешно созданы!") 