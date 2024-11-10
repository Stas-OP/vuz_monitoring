from django.contrib import admin
from .models import ComplaintStatus, Building, Department, Complaint

# Register your models here.
admin.site.register(ComplaintStatus)
admin.site.register(Building)
admin.site.register(Department)
admin.site.register(Complaint)
