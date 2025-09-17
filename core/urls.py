from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('estoque/', views.estoque, name='estoque'),
    path('carro/<int:pk>/', views.detalhe_carro, name='detalhe_carro'),
    path('sobre/', views.sobre, name='sobre'),
    path('buscar/', views.buscar, name='buscar'),
]
