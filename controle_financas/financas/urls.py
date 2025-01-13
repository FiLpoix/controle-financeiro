from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_transacoes, name='lista_transacoes'),
    path('cadastro/', views.cadastrar_transacao, name='cadastro_transacao'),
    path('filtro/', views.filtrar_transacoes, name='filtro_transacoes'),
]