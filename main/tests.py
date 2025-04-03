from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Complaint, Building, Department, ComplaintStatus

class ModelTests(TestCase):
    """Тесты для моделей системы"""
    
    def setUp(self):
        """Подготовка тестовых данных"""
        self.status = ComplaintStatus.objects.create(name="Новая")
        self.building = Building.objects.create(number=1, name="Главный корпус")
        self.department = Department.objects.create(name="Кафедра информатики")
    
    def test_complaint_status_str(self):
        """Тест строкового представления модели ComplaintStatus"""
        self.assertEqual(str(self.status), "Новая")
    
    def test_building_str(self):
        """Тест строкового представления модели Building"""
        self.assertEqual(str(self.building), "Корпус №1")
    
    def test_department_str(self):
        """Тест строкового представления модели Department"""
        self.assertEqual(str(self.department), "Кафедра информатики")
    
    def test_complaint_creation(self):
        """Тест создания жалобы"""
        complaint = Complaint.objects.create(
            title="Тестовая жалоба",
            description="Описание тестовой жалобы",
            building=self.building,
            department=self.department,
            status=self.status
        )
        self.assertEqual(complaint.title, "Тестовая жалоба")
        self.assertEqual(complaint.building, self.building)
        self.assertEqual(complaint.department, self.department)
        self.assertEqual(complaint.status, self.status)

class ViewTests(TestCase):
    """Тесты для представлений системы"""
    
    def setUp(self):
        """Подготовка тестовых данных"""
        self.client = Client()
        self.status = ComplaintStatus.objects.create(name="Новая")
        self.building = Building.objects.create(number=1, name="Главный корпус")
        self.department = Department.objects.create(name="Кафедра информатики")
        
        # Создание тестовых пользователей
        self.admin_user = User.objects.create_user(
            username='admin', 
            password='admin', 
            is_staff=True,
            is_superuser=True
        )
        
        self.manager_user = User.objects.create_user(
            username='manager', 
            password='manager'
        )
    
    def test_submit_complaint_page_loads(self):
        """Тест загрузки страницы подачи жалобы"""
        response = self.client.get(reverse('submit_complaint'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'submit_complaint.html')
    
    def test_submit_complaint_creation(self):
        """Тест создания жалобы через форму"""
        complaint_data = {
            'title': 'Тестовая жалоба',
            'description': 'Описание тестовой жалобы',
            'building': self.building.id,
            'department': self.department.id,
        }
        
        response = self.client.post(reverse('submit_complaint'), complaint_data)
        self.assertEqual(response.status_code, 302)  # Redirect после успешного создания
        
        # Проверим, что жалоба создалась
        self.assertEqual(Complaint.objects.count(), 1)
        complaint = Complaint.objects.first()
        self.assertEqual(complaint.title, 'Тестовая жалоба')
        self.assertEqual(complaint.status.name, 'Новая')
    
    def test_manager_login(self):
        """Тест входа менеджера"""
        login_data = {
            'username': 'manager',
            'password': 'manager'
        }
        
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 302)  # Redirect после успешного входа
        self.assertEqual(response.url, reverse('manager_panel'))
    
    def test_admin_login(self):
        """Тест входа администратора"""
        login_data = {
            'username': 'admin',
            'password': 'admin'
        }
        
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 302)  # Redirect после успешного входа
        self.assertEqual(response.url, reverse('admin_panel'))
    
    def test_update_complaint_status(self):
        """Тест обновления статуса жалобы"""
        # Создаем жалобу
        complaint = Complaint.objects.create(
            title="Тестовая жалоба",
            description="Описание тестовой жалобы",
            building=self.building,
            department=self.department,
            status=self.status
        )
        
        # Создаем новый статус
        new_status = ComplaintStatus.objects.create(name="В процессе")
        
        # Авторизуемся как менеджер
        self.client.login(username='manager', password='manager')
        
        # Обновляем статус
        response = self.client.post(
            reverse('update_status', args=[complaint.id]), 
            {'status': new_status.id}
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect после успешного обновления
        
        # Проверяем обновление статуса
        complaint.refresh_from_db()
        self.assertEqual(complaint.status, new_status)
        
    def test_empty_complaint_submission(self):
        """Тест отправки пустой формы жалобы"""
        response = self.client.post(reverse('submit_complaint'), {})
        
        # Проверяем, что форма не отправляется и возвращается на страницу формы
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'submit_complaint.html')
        
        # Проверяем, что жалоба не создалась
        self.assertEqual(Complaint.objects.count(), 0)
        
        # Проверяем наличие сообщения об ошибке
        self.assertContains(response, 'Все поля должны быть заполнены')
    
    def test_invalid_building_submission(self):
        """Тест отправки жалобы с несуществующим зданием"""
        complaint_data = {
            'title': 'Тестовая жалоба',
            'description': 'Описание тестовой жалобы',
            'building': 999,  # несуществующий ID здания
            'department': self.department.id,
        }
        
        response = self.client.post(reverse('submit_complaint'), complaint_data)
        
        # Проверяем, что форма не отправляется и возвращается ошибка
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'submit_complaint.html')
        
        # Проверяем, что жалоба не создалась
        self.assertEqual(Complaint.objects.count(), 0)
        
        # Проверяем наличие сообщения об ошибке
        self.assertContains(response, 'Выбрано несуществующее здание или департамент')
    
    def test_title_length_validation(self):
        """Тест валидации длины заголовка жалобы"""
        # Создаем заголовок длиной более 200 символов
        long_title = 'A' * 201
        
        complaint_data = {
            'title': long_title,
            'description': 'Описание тестовой жалобы',
            'building': self.building.id,
            'department': self.department.id,
        }
        
        response = self.client.post(reverse('submit_complaint'), complaint_data)
        
        # Проверяем, что форма не отправляется и возвращается ошибка
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'submit_complaint.html')
        
        # Проверяем, что жалоба не создалась
        self.assertEqual(Complaint.objects.count(), 0)
        
        # Проверяем наличие сообщения об ошибке
        self.assertContains(response, 'Заголовок не должен превышать 200 символов')

class SecurityTests(TestCase):
    """Тесты для проверки безопасности системы"""
    
    def setUp(self):
        """Подготовка тестовых данных"""
        self.client = Client()
        
        # Создание тестовых пользователей
        self.admin_user = User.objects.create_user(
            username='admin', 
            password='admin', 
            is_staff=True,
            is_superuser=True
        )
        
        self.manager_user = User.objects.create_user(
            username='manager', 
            password='manager'
        )
    
    def test_manager_panel_access_unauthorized(self):
        """Тест доступа к панели менеджера без авторизации"""
        response = self.client.get(reverse('manager_panel'))
        
        # Ожидаем перенаправление на страницу логина
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/login/' in response.url)
    
    def test_admin_panel_access_unauthorized(self):
        """Тест доступа к панели администратора без авторизации"""
        response = self.client.get(reverse('admin_panel'))
        
        # Ожидаем перенаправление на страницу логина
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/login/' in response.url)
    
    def test_admin_panel_access_as_manager(self):
        """Тест доступа к панели администратора с правами менеджера"""
        # Авторизуемся как менеджер
        self.client.login(username='manager', password='manager')
        
        response = self.client.get(reverse('admin_panel'))
        
        # Ожидаем перенаправление на панель менеджера
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('manager_panel'))
