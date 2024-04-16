"""
URL configuration for config project.

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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import DogsCreate, DogsUpdateView, DogsDetailView, DogsDelete
from django.views.static import serve
from django.urls import re_path


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('main.urls')),  # Включаем урлы из приложения main
    path('users/', include('users.urls', namespace='users')),  # Включаем урлы из приложения user
    path('drag_and_drop_app/', include('drag_and_drop_app.urls', namespace='drag_and_drop_app')),  # Включаем урлы из приложения drag_and_drop_app

    path('history/', include('history.urls', namespace='history')),  # Включаем урлы из приложения history

    path('create_dogs', DogsCreate.as_view(), name='create_dogs'),
    path('detail_dogs/<int:pk>', DogsDetailView.as_view(), name='dogs_detail'),
    path('update_dogs/<int:pk>', DogsUpdateView.as_view(), name='dogs_update'),
    path('dogs_delete/<int:pk>', DogsDelete.as_view(), name='dogs_delete_com'),  # Удаление соревнования

    path('roles/', include('roles.urls', namespace='roles')),  # ссылки ролей
    path('news/', include('news.urls', namespace='news')),  # ссылки новостей

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'
    ),
    
    re_path(r'^images/(?P<path>.*)$', serve, {'document_root': str(settings.BASE_DIR / 'images')}),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
