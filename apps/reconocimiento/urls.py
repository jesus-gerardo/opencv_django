from django.urls import path
from . import views

urlpatterns = [
    path('reconocimiento/imagen', views.get_imagen_post)
]