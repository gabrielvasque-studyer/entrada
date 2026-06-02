from django.urls import path
from .views import listar_entradas, cadastrar_entrada, excluirEntrada, editarEntrada

urlpatterns = [
    path('listarentradas', listar_entradas),
    path('cadastrarentrada', cadastrar_entrada),
    path('excluirEntrada/<int:id>', excluirEntrada),
    path('editarEntrada/<int:id>', editarEntrada),
    
]
