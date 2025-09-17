from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Carro, Marca, ImagemSite


def home(request):
    """View da página inicial"""
    carros_destaque = Carro.objects.filter(destaque=True, condicao__in=['novo', 'seminovo'])[:6]
    marcas = Marca.objects.filter(ativa=True).order_by('ordem', 'nome')
    
    # Buscar imagem do carro flutuante
    carro_flutuante = ImagemSite.objects.filter(
        tipo='carro_flutuante', 
        ativo=True
    ).order_by('ordem').first()
    
    context = {
        'carros_destaque': carros_destaque,
        'marcas': marcas,
        'carro_flutuante': carro_flutuante,
        'total_carros': Carro.objects.filter(condicao__in=['novo', 'seminovo']).count(),
        'anos_experiencia': 15,
        'clientes_satisfeitos': 500,
    }
    return render(request, 'core/home.html', context)


def estoque(request):
    """View da página de estoque com paginação"""
    carros_list = Carro.objects.filter(condicao__in=['novo', 'seminovo']).order_by('-criado_em')
    
    # Filtros
    fabricante = request.GET.get('fabricante')
    condicao = request.GET.get('condicao')
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')
    
    if fabricante:
        carros_list = carros_list.filter(fabricante__icontains=fabricante)
    
    if condicao:
        carros_list = carros_list.filter(condicao=condicao)
    
    if preco_min:
        carros_list = carros_list.filter(preco__gte=preco_min)
    
    if preco_max:
        carros_list = carros_list.filter(preco__lte=preco_max)
    
    # Paginação - 6 carros por página
    paginator = Paginator(carros_list, 6)
    page_number = request.GET.get('page')
    carros = paginator.get_page(page_number)
    
    # Fabricantes únicos para filtro
    fabricantes = Carro.objects.values_list('fabricante', flat=True).distinct().order_by('fabricante')
    
    context = {
        'carros': carros,
        'fabricantes': fabricantes,
        'filtros': {
            'fabricante': fabricante,
            'condicao': condicao,
            'preco_min': preco_min,
            'preco_max': preco_max,
        }
    }
    return render(request, 'core/estoque.html', context)


def detalhe_carro(request, pk):
    """View dos detalhes do carro"""
    carro = get_object_or_404(Carro, pk=pk)
    
    # Carros relacionados (mesmo fabricante, excluindo o atual)
    carros_relacionados = Carro.objects.filter(
        fabricante=carro.fabricante,
        condicao__in=['novo', 'seminovo']
    ).exclude(pk=carro.pk)[:3]
    
    context = {
        'carro': carro,
        'carros_relacionados': carros_relacionados,
    }
    return render(request, 'core/detalhe_carro.html', context)


def sobre(request):
    """View da página sobre"""
    # Buscar imagem da loja para a página sobre
    imagem_loja = ImagemSite.objects.filter(
        tipo='sobre_loja', 
        ativo=True
    ).order_by('ordem').first()
    
    context = {
        'imagem_loja': imagem_loja,
        'anos_experiencia': 15,
        'carros_vendidos': 800,
        'clientes_satisfeitos': 500,
    }
    return render(request, 'core/sobre.html', context)


def buscar(request):
    """View para busca de carros"""
    query = request.GET.get('q')
    carros = []
    
    if query:
        carros = Carro.objects.filter(
            Q(modelo__icontains=query) |
            Q(fabricante__icontains=query) |
            Q(descricao__icontains=query),
            condicao__in=['novo', 'seminovo']
        ).order_by('-criado_em')
        
        # Paginação
        paginator = Paginator(carros, 6)
        page_number = request.GET.get('page')
        carros = paginator.get_page(page_number)
    
    context = {
        'carros': carros,
        'query': query,
    }
    return render(request, 'core/buscar.html', context)
