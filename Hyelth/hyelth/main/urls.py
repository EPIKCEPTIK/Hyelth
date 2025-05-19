"""
URL configuration for hyelth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.urls import path
from . import  views
from django.conf.urls.static import  static
from django.conf import  settings
urlpatterns = [
    path('', views.cabinet, name='cabinet'),
    path('schedule', views.schedule, name='schedule'),
    path('prescriptions', views.prescriptions, name='prescriptions'),
    path('find_medicine', views.find_medicine, name='find_medicine'),
    path('registration', views.registration, name='registration'),
    path('login', views.login, name="login"),
    path('logout', views.user_logout, name="user_logout"),
    path('medicine/<int:pk>/', views.MedicineDetailView.as_view(), name='medicine_details'),
    path('add_medicine/<str:id>/<str:date>',views.add_medicine, name="add_medicine")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)