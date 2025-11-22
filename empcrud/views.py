from email.mime import message
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from .models import EmployeeDetail, User , Project , Task
from .forms import *
from django.contrib import messages
from django.db.models import Count
from django.db import transaction



'''def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password, email=email)
            auth_login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})'''

def login_view(request):
    error_message = ''
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(username=email, password=password)
            if user is not None:
                auth_login(request, user)
                if user.is_staff:
                    return redirect('detail')
                else:   
                    return redirect('empdetail')
            else:
                error_message = 'Invalid email or password'
        else:
            error_message = 'Please provide both email and password'
    
    return render(request, 'login.html', {'error_message': error_message})

@login_required(login_url='login')
def detail(request):
    form = EmployeeForm()
    employees_with_users = EmployeeDetail.objects.select_related('emp_user').all()
    department_counts = EmployeeDetail.objects.values('emp_department').annotate(
        employee_count=Count('emp_id')
    ).order_by('emp_department')
    department_counts = [
        {'name': dept['emp_department'], 'employee_count': dept['employee_count']}
        for dept in department_counts
    ]
    project = Project.objects.all()
    task = Task.objects.all()
    
    context ={
        'form' : form,
        'department_counts' : department_counts,
        'employees_with_users' : employees_with_users, 
        'project': project,
        'task': task,
    }
    return render(request , 'detail.html' , context)


@login_required
def empdetail(request):
    form = EmployeeForm()
    detail = EmployeeDetail.objects.filter(emp_user = request.user)

    try:
        employee = EmployeeDetail.objects.select_related('emp_user').get(emp_user = request.user)
        
    except EmployeeDetail.DoesNotExist:
        raise ValueError('employee doesnot exit')
    context = {
        'employee' : employee,
    }
    return render(request, 'employe.html', context)


@login_required
@transaction.atomic
@staff_member_required
def create(request):
    user = UserForm()
    form = EmployeeForm()
    if request.method == 'POST':
        user = UserForm(request.POST)
        form = EmployeeForm(request.POST)
        if user.is_valid() and form.is_valid():
            new_user = user.save()
            emp = form.save(commit=False)   
            emp.emp_user = new_user
            emp.save()
            messages.success(request, "Employee created successfully!")
            return redirect('detail')
        else:
            form = EmployeeForm()
    emp = EmployeeDetail.objects.all()
    context={
        'form' : form ,
        'emp' : emp,
        'user' : user
    }
    return render(request , 'create.html' , context)
    
@login_required
def edit_profile(request , pk=None):
    if request.method == 'POST':
        emp = EmployeeDetail.objects.get(pk=pk)
        form = EmployeeForm(request.POST , instance=emp)
        if form.is_valid():
            form.save()
            return redirect('detail')
    else:
        emp = EmployeeDetail.objects.get(pk=pk)
        form = EmployeeForm(instance=emp)
    return render(request , 'edit_profile.html' , {'form':form})

@login_required
def delete_profile(request , pk=None):
    if request.method == 'POST':
        emp = EmployeeDetail.objects.get(pk=pk)
        emp.delete()
        return redirect('detail')
    emp = EmployeeDetail.objects.get(pk=pk)
    return render(request, 'delete_profile.html', {'employee': emp})

@login_required
def department(request):
    detail = EmployeeDetail.objects.all()
    department_counts = EmployeeDetail.objects.values('emp_department').annotate(
        employee_count=Count('emp_id')
    ).order_by('emp_department')
    department_counts = [
        {'name': dept['emp_department'], 'employee_count': dept['employee_count']}
        for dept in department_counts
    ]
    combined_data = zip(detail, department_counts)
    return render(request, 'department.html', { 
        'combined_data': combined_data,
    })

@login_required
def ProjectView(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('detail')
    else:
        form = ProjectForm()
    return render(request , 'project.html' , {'form' : form})
    
@login_required
def Project_delete(request , pk=None):
    if request.method == 'POST':
        pro = Project.objects.get(pk=pk)
        pro.delete()
        return redirect('detail')
    if pk is None:
        return redirect('project')
    pro = Project.objects.get(pk=pk)
    return render(request , 'project_del.html' ,{'project' : pro})
        
@login_required
def Task_assign(request):    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully!')
            return redirect('detail')
        else:
            messages.error(request, 'The Task could not be created because the data didn\'t validate.')
    else:
        form = TaskForm()
    return render(request , 'Task.html' , {'form' : form})
    


@login_required
def LogoutView(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


        


