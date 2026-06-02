from django.contrib import admin
from .models import Fornecedor, Produto, Entrada

admin.site.register(Fornecedor)
admin.site.register(Produto)
admin.site.register(Entrada)