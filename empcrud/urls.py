from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', login_view, name='login'),
    path('detail', detail, name='detail'),
    path('create', create, name='create'),
    path('edit_profile/<int:pk>/', edit_profile, name='edit_profile'),
    path('delete_profile/<int:pk>/', delete_profile, name='delete_profile'),
    #path('register', register, name='register'),
    path('department', department, name='department'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('empdetail' , empdetail , name = 'empdetail'),
    path('project' , ProjectView , name='project'),
    path('project_delete/<int:pk>/', Project_delete, name='project_delete'),
    path('task' , Task_assign , name='Task')
]
