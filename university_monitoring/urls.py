"""
URL configuration for university_monitoring project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
from django.conf import settings # Импорт настроек
from django.conf.urls.static import static # Импорт функции static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.submit_complaint, name='submit_complaint'),
    path('manager/', views.manager_panel, name='manager_panel'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('update-status/<int:complaint_id>/', views.update_status, name='update_status'),
    path('delete-complaint/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
]

# Добавляем обработку медиа-файлов только в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
