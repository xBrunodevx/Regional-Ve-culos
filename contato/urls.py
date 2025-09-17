from django.urls import path
from . import views

app_name = 'contato'

urlpatterns = [
    path('contato/', views.contato, name='contato'),
    path('financiamento/', views.financiamento, name='financiamento'),
    path('financiamento/<int:carro_id>/', views.financiamento, name='financiamento_carro'),
]
