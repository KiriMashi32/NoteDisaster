"""
URL configuration for note_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_note/', views.create_note, name='create_note'),
    path('ma_vue/', views.ma_vue, name='ma_vue'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True, next_page='view_notes'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html', next_page='login'), name='logout'),
    path('notes/', views.view_notes, name='view_notes'),
    path('edit_note/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('toggle_task/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)