from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.ViewTaskList, name="view_task_list"),
    path('create_task/', views.CreateTask, name='create_task'),
    path('task_details/<int:task_id>', views.TaskDetails, name='task_details'),
    path('update_task/<int:task_id>', views.UpdateTask, name='update_task'),
    path('delete_task/<int:task_id>', views.DeleteTask, name='delete_task'),
    path('mark_complete/<int:task_id>', views.TaskMarkComplete, name='mark_complete'),
    path('profile/', views.ProfileView, name='profile'), 
    
    path('register/', views.register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
]