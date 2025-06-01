from django.urls import path
from . import views
from .views import submit_project, register
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='projects'),
    path("submit_project/", submit_project, name="submit_project"),
    path('contact/', views.contact_view, name='contact'),
    path('projects/', views.project_list, name='project_list'),
    path('add-project/', views.add_project, name='add_project'),
    path("contact/", views.contact_view, name="contact"),
    path("api/project/", submit_project, name="submit_project"),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
   
    





]
