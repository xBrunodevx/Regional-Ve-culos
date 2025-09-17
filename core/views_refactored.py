"""
Views para o app Core - Regional Veículos
Implementa as principais páginas do site seguindo princípios SOLID
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, QuerySet
from typing import Dict, Any, Optional

from .models import Carro, Marca, ImagemSite


class CarroService:
    """Serviço para operações relacionadas a carros"""
    
    @staticmethod
    def get_carros_disponiveis() -> QuerySet:
        """Retorna carros disponíveis para venda"""
        return Carro.objects.filter(condicao__in=['novo', 'seminovo'])
    
    @staticmethod
    def get_carros_destaque(limit: int = 6) -> QuerySet:
        """Retorna carros em destaque limitados"""
        return CarroService.get_carros_disponiveis().filter(destaque=True)[:limit]
    
    @staticmethod
    def get_fabricantes_disponiveis() -> QuerySet:
        """Retorna lista de fabricantes com carros disponíveis"""
        return Carro.objects.values_list('fabricante', flat=True).distinct().order_by('fabricante')
    
    @staticmethod
    def aplicar_filtros(queryset: QuerySet, filtros: Dict[str, Any]) -> QuerySet:
        """Aplica filtros ao queryset de carros"""
        if filtros.get('fabricante'):
            queryset = queryset.filter(fabricante__icontains=filtros['fabricante'])
        
        if filtros.get('condicao'):
            queryset = queryset.filter(condicao=filtros['condicao'])
        
        if filtros.get('preco_min'):
            queryset = queryset.filter(preco__gte=filtros['preco_min'])
        
        if filtros.get('preco_max'):
            queryset = queryset.filter(preco__lte=filtros['preco_max'])
        
        return queryset
    
    @staticmethod
    def buscar_carros(query: str) -> QuerySet:
        """Busca carros por termo de pesquisa"""
        if not query:
            return Carro.objects.none()
        
        return CarroService.get_carros_disponiveis().filter(
            Q(modelo__icontains=query) |
            Q(fabricante__icontains=query) |
            Q(descricao__icontains=query)
        ).order_by('-criado_em')
    
    @staticmethod
    def get_carros_relacionados(carro: Carro, limit: int = 3) -> QuerySet:
        """Retorna carros relacionados (mesmo fabricante)"""
        return CarroService.get_carros_disponiveis().filter(
            fabricante=carro.fabricante
        ).exclude(pk=carro.pk)[:limit]


class ImagemService:
    """Serviço para operações relacionadas a imagens"""
    
    @staticmethod
    def get_imagem_por_tipo(tipo: str) -> Optional[ImagemSite]:
        """Busca imagem ativa por tipo"""
        return ImagemSite.objects.filter(
            tipo=tipo,
            ativo=True
        ).order_by('ordem').first()


def home(request):
    """
    Página inicial do site
    Exibe carros em destaque, marcas e estatísticas
    """
    context = {
        'carros_destaque': CarroService.get_carros_destaque(),
        'marcas': Marca.objects.filter(ativa=True).order_by('ordem', 'nome'),
        'carro_flutuante': ImagemService.get_imagem_por_tipo('carro_flutuante'),
        'total_carros': CarroService.get_carros_disponiveis().count(),
        'anos_experiencia': 15,
        'clientes_satisfeitos': 500,
    }
    return render(request, 'core/home.html', context)


def estoque(request):
    """
    Página de estoque com filtros e paginação
    Permite filtrar carros por fabricante, condição e preço
    """
    # Extrair filtros da requisição
    filtros = {
        'fabricante': request.GET.get('fabricante'),
        'condicao': request.GET.get('condicao'),
        'preco_min': request.GET.get('preco_min'),
        'preco_max': request.GET.get('preco_max'),
    }
    
    # Aplicar filtros
    carros_queryset = CarroService.get_carros_disponiveis().order_by('-criado_em')
    carros_filtrados = CarroService.aplicar_filtros(carros_queryset, filtros)
    
    # Configurar paginação
    paginator = Paginator(carros_filtrados, 6)
    page_number = request.GET.get('page')
    carros = paginator.get_page(page_number)
    
    context = {
        'carros': carros,
        'fabricantes': CarroService.get_fabricantes_disponiveis(),
        'filtros': filtros,
    }
    return render(request, 'core/estoque.html', context)


def detalhe_carro(request, pk: int):
    """
    Página de detalhes de um carro específico
    Inclui carros relacionados do mesmo fabricante
    """
    carro = get_object_or_404(Carro, pk=pk)
    
    context = {
        'carro': carro,
        'carros_relacionados': CarroService.get_carros_relacionados(carro),
    }
    return render(request, 'core/detalhe_carro.html', context)


def sobre(request):
    """
    Página institucional sobre a empresa
    Exibe informações, estatísticas e imagem da loja
    """
    context = {
        'imagem_loja': ImagemService.get_imagem_por_tipo('sobre_loja'),
        'anos_experiencia': 15,
        'carros_vendidos': 800,
        'clientes_satisfeitos': 500,
    }
    return render(request, 'core/sobre.html', context)


def buscar(request):
    """
    Página de resultados de busca
    Permite pesquisar carros por modelo, fabricante ou descrição
    """
    query = request.GET.get('q', '').strip()
    carros = Carro.objects.none()
    
    if query:
        carros_resultado = CarroService.buscar_carros(query)
        
        # Configurar paginação para resultados
        paginator = Paginator(carros_resultado, 6)
        page_number = request.GET.get('page')
        carros = paginator.get_page(page_number)
    
    context = {
        'carros': carros,
        'query': query,
    }
    return render(request, 'core/buscar.html', context)
