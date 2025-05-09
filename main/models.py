from django.db import models

# Create your models here.

class ComplaintStatus(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Building(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Корпус №{self.number}"

class Department(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Complaint(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    status = models.ForeignKey(ComplaintStatus, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='complaint_photos/', blank=True, null=True)
    # Поля для контактных данных
    contact_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Имя контакта")
    contact_info = models.CharField(max_length=200, blank=True, null=True, verbose_name="Контактная информация (email/телефон)")
    
    def __str__(self):
        return self.title
