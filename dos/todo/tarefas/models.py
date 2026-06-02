from django.db import models

class Entrada(models.Model):
    # Relacionamos com o produto e fornecedor
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    fornecedor = models.ForeignKey('Fornecedor', on_delete=models.CASCADE)
    
    quantidade = models.IntegerField()
    preco_custo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    data_entrada = models.DateField()
    nfe = models.CharField(max_length=50)
    observacao = models.CharField(max_length=250, blank=True, null=True)

    def valor_total(self):
        return self.quantidade * self.preco_custo_unitario

    def __str__(self):
        return f"Entrada {self.id} - {self.produto.nome}"
    
class Fornecedor(models.Model):
    nome_fantasia = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.nome_fantasia

# MÓDULO 1: PRODUTO (Criado aqui para referência)
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    sku = models.CharField(max_length=20, unique=True)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    # Este campo é essencial para o seu módulo de Entrada atualizar
    estoque_atual = models.IntegerField(default=0) 

    def __str__(self):
        return self.nome