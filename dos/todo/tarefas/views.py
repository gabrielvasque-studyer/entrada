from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Entrada, Produto, Fornecedor
from django.db.models import Q
    
def cadastrar_entrada(request):
    if request.method == "POST":
        # Pega os dados do formulário HTML
        id_produto = request.POST.get('produto')
        id_fornecedor = request.POST.get('fornecedor')
        qtd = request.POST.get('quantidade')
        preco_vinda_html = request.POST.get('preco_custo') # Ex: "1.500,50"
        data = request.POST.get('data')
        nfe = request.POST.get('nfe')
        obs = request.POST.get('observacao')

        # --- LIMPEZA MANUAL DO PREÇO ---
        # Remove o ponto de milhar e troca a vírgula pelo ponto decimal do Python
        preco_limpo = preco_vinda_html.replace('.', '').replace(',', '.')

        # 1. Cria o registro de entrada
        nova_entrada = Entrada(
            produto_id=id_produto,
            fornecedor_id=id_fornecedor,
            quantidade=int(qtd),
            preco_custo_unitario=preco_limpo,
            data_entrada=data,
            nfe=nfe,
            observacao=obs
        )
        nova_entrada.save()

        # 2. Atualiza o estoque do produto
        produto = Produto.objects.get(id=id_produto)
        produto.estoque_atual += int(qtd)
        produto.save()

        return HttpResponseRedirect('/tarefas/listarentradas')

    # Se for GET, busca os dados para os selects do formulário
    return render(request, 'cadastroEntrada.html', {
        'produtos': Produto.objects.all(),
        'fornecedores': Fornecedor.objects.all()
    })

def listar_entradas(request):
    termo_pesquisa = request.GET.get('search')
    
    if termo_pesquisa:
        if "/" in termo_pesquisa:
            try:
                # Se o usuário digitou 24/05/2026, vira 2026-05-24
                termo_pesquisa = datetime.strptime(termo_pesquisa, '%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError:
                # Se não for uma data válida (ex: 99/99/9999), mantém o termo original para não travar
                pass

        # Filtra pelo nome do produto, número da nota fiscal, fornecedor, observação ou data
        entradas = Entrada.objects.filter(
            Q(produto__nome__icontains=termo_pesquisa) | 
            Q(nfe__icontains=termo_pesquisa) |
            Q(fornecedor__nome_fantasia__icontains=termo_pesquisa) |
            Q(observacao__icontains=termo_pesquisa) |
            Q(data_entrada__icontains=termo_pesquisa)
        )

        
    else:
        entradas = Entrada.objects.all().order_by('-data_entrada') # As mais recentes primeiro

    return render(request, "listarEntradas.html", {'entradas': entradas})

def excluirEntrada(request, id):
    # Busca a entrada
    entrada = Entrada.objects.get(id=id)
    
    # Lógica de estorno para o estoque não ficar errado
    produto = entrada.produto
    produto.estoque_atual -= entrada.quantidade
    produto.save()
    
    # Deleta e redireciona no padrão do prof
    entrada.delete()
    return HttpResponseRedirect("/tarefas/listarentradas")

def editarEntrada(request, id):
    if request.method == "POST":
        # Captura os dados do formulário
        id_produto = request.POST.get('produto')
        id_fornecedor = request.POST.get('fornecedor')
        quantidade_nova = int(request.POST.get('quantidade'))
        preco_vinda_html = request.POST.get('preco_custo')
        nfe = request.POST.get('nfe')
        data = request.POST.get('data')
        obs = request.POST.get('observacao')

        # --- LIMPEZA MANUAL DO PREÇO ---
        preco_limpo = preco_vinda_html.replace('.', '').replace(',', '.')

        # Busca a entrada existente para atualizar
        editar_entrada = Entrada.objects.get(id=id)

        # 1. Estorno do estoque antigo (Módulo 4)
        produto_antigo = editar_entrada.produto
        produto_antigo.estoque_atual -= editar_entrada.quantidade
        produto_antigo.save()

        # 2. Atualiza os campos do objeto
        editar_entrada.produto_id = id_produto
        editar_entrada.fornecedor_id = id_fornecedor
        editar_entrada.quantidade = quantidade_nova
        editar_entrada.preco_custo_unitario = preco_limpo
        editar_entrada.nfe = nfe
        editar_entrada.data_entrada = data
        editar_entrada.observacao = obs
        editar_entrada.save()

        # 3. Aplica o novo estoque atualizado
        novo_produto = editar_entrada.produto
        novo_produto.estoque_atual += quantidade_nova
        novo_produto.save()

        return HttpResponseRedirect('/tarefas/listarentradas')
    else:
        # Se for GET, busca a entrada e os dados para preencher o formulário
        entrada = Entrada.objects.get(id=id)
        produtos = Produto.objects.all()
        fornecedores = Fornecedor.objects.all()

        return render(request, "editarEntrada.html", {
            'entrada': entrada,
            'produtos': produtos,
            'fornecedores': fornecedores
        })