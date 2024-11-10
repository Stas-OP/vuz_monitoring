from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import Complaint, Building, Department, ComplaintStatus

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username == 'manager' and password == 'manager':
            user, created = User.objects.get_or_create(username='manager')
            if created:
                user.set_password('manager')
                user.is_staff = False
                user.is_superuser = False
                user.save()
            login(request, user)
            return redirect('manager_panel')
        elif username == 'admin' and password == 'admin':
            user, created = User.objects.get_or_create(username='admin')
            if created:
                user.set_password('admin')
                user.is_staff = True
                user.is_superuser = True
                user.save()
            login(request, user)
            return redirect('admin_panel')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})
    
    return render(request, 'login.html')

def submit_complaint(request):
    if request.method == 'POST':
        complaint = Complaint.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            building_id=request.POST['building'],
            department_id=request.POST['department'],
            status=ComplaintStatus.objects.get(name='Новая')
        )
        return redirect('submit_complaint')
    
    buildings = Building.objects.all()
    departments = Department.objects.all()
    return render(request, 'submit_complaint.html', {
        'buildings': buildings,
        'departments': departments
    })

@login_required
def manager_panel(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    statuses = ComplaintStatus.objects.all()
    return render(request, 'manager_panel.html', {
        'complaints': complaints,
        'statuses': statuses
    })

@login_required
def admin_panel(request):
    if not request.user.is_superuser:
        return redirect('manager_panel')
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'admin_panel.html', {'complaints': complaints})

@login_required
def update_status(request, complaint_id):
    if request.method == 'POST':
        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.status_id = request.POST['status']
        complaint.save()
    return redirect('manager_panel')

@login_required
def delete_complaint(request, complaint_id):
    if request.method == 'POST':
        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.delete()
    return redirect('admin_panel')

def logout_view(request):
    logout(request)
    return redirect('submit_complaint')
