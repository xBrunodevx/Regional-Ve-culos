from django.contrib import sitemaps
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from .models import Carro

class StaticViewSitemap(sitemaps.Sitemap):
    """Sitemap para páginas estáticas"""
    priority = 1.0
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ['core:home', 'core:estoque', 'core:sobre', 'contato:contato', 'contato:financiamento']

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        """Data da última modificação"""
        return timezone.now()

    def priority_func(self, item):
        """Prioridade baseada na página"""
        priorities = {
            'core:home': 1.0,
            'core:estoque': 0.9,
            'contato:financiamento': 0.8,
            'contato:contato': 0.8,
            'core:sobre': 0.7,
        }
        return priorities.get(item, 0.5)

class CarroSitemap(sitemaps.Sitemap):
    """Sitemap para páginas de carros individuais"""
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Carro.objects.filter(disponivel=True).select_related('marca')

    def lastmod(self, obj):
        """Data da última modificação do carro"""
        return obj.data_cadastro

    def location(self, obj):
        return reverse('core:detalhe_carro', args=[obj.id])

    def priority_func(self, obj):
        """Prioridade baseada no destaque do carro"""
        return 0.9 if obj.destaque else 0.7

class EstoqueSitemap(sitemaps.Sitemap):
    """Sitemap para páginas de estoque filtradas"""
    changefreq = 'daily'
    priority = 0.6
    protocol = 'https'

    def items(self):
        """URLs de estoque por marca"""
        marcas = Carro.objects.filter(disponivel=True).values_list('marca__nome', flat=True).distinct()
        return [f"estoque-{marca.lower()}" for marca in marcas if marca]

    def location(self, item):
        marca = item.replace('estoque-', '')
        return f"{reverse('core:estoque')}?fabricante={marca}"

    def lastmod(self, item):
        return timezone.now()

# Configuração do sitemap
sitemaps = {
    'static': StaticViewSitemap,
    'carros': CarroSitemap,
    'estoque': EstoqueSitemap,
}
