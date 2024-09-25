# mi_aplicacion/urls.py (si no existe, créalo)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
