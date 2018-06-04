"""Sensores URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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


from sensors import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', views.read_csv, name='upload_file'),
    path('sensors/', views.get_sensors, name='sensors'),
    path('sensors/<str:sensor_id>', views.get_signals, name='sensors_signals'),
    path('sensors/<str:sensor_id>/readings', views.get_readings, name='readings'),
]
