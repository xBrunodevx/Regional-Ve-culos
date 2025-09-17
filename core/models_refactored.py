"""
Models para o app Core - Regional Veículos
Define as entidades principais do sistema seguindo Domain-Driven Design
"""

from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from typing import List


class TimeStampedModel(models.Model):
    """
    Modelo abstrato que adiciona campos de timestamp
    para auditoria de criação e modificação
    """
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )
    
    class Meta:
        abstract = True


class Marca(TimeStampedModel):
    """
    Representa uma marca de veículo
    Controla a exibição e ordenação das marcas no site
    """
    nome = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Nome da Marca',
        help_text='Nome da marca do veículo'
    )
    logo = models.ImageField(
        upload_to='marcas/',
        verbose_name='Logo da Marca',
        help_text='Logo da marca em formato SVG ou PNG'
    )
    ativa = models.BooleanField(
        default=True,
        verbose_name='Marca Ativa',
        help_text='Marca visível no site'
    )
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem de Exibição',
        help_text='Ordem de exibição no site (menor número aparece primeiro)'
    )
    
    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['ordem', 'nome']
        indexes = [
            models.Index(fields=['ativa', 'ordem']),
        ]
    
    def __str__(self) -> str:
        return self.nome
    
    @property
    def carros_disponiveis_count(self) -> int:
        """Retorna número de carros disponíveis desta marca"""
        return self.carros.filter(condicao__in=['novo', 'seminovo']).count()


class Carro(TimeStampedModel):
    """
    Representa um veículo no estoque
    Contém todas as informações técnicas e comerciais
    """
    
    class CondicaoChoices(models.TextChoices):
        NOVO = 'novo', 'Novo'
        SEMINOVO = 'seminovo', 'Seminovo'
        VENDIDO = 'vendido', 'Vendido'
    
    class CombustivelChoices(models.TextChoices):
        FLEX = 'flex', 'Flex'
        GASOLINA = 'gasolina', 'Gasolina'
        ETANOL = 'etanol', 'Etanol'
        DIESEL = 'diesel', 'Diesel'
        ELETRICO = 'eletrico', 'Elétrico'
        HIBRIDO = 'hibrido', 'Híbrido'
    
    class CambioChoices(models.TextChoices):
        MANUAL = 'manual', 'Manual'
        AUTOMATICO = 'automatico', 'Automático'
        CVT = 'cvt', 'CVT'
        AUTOMATIZADO = 'automatizado', 'Automatizado'
    
    # Informações básicas
    modelo = models.CharField(
        max_length=100,
        verbose_name='Modelo',
        db_index=True
    )
    fabricante = models.CharField(
        max_length=50,
        verbose_name='Fabricante',
        db_index=True
    )
    ano = models.PositiveIntegerField(
        verbose_name='Ano',
        validators=[
            MinValueValidator(1990),
            MaxValueValidator(2030)
        ]
    )
    cor = models.CharField(
        max_length=30,
        verbose_name='Cor'
    )
    
    # Detalhes técnicos
    quilometragem = models.PositiveIntegerField(
        verbose_name='Quilometragem',
        help_text='Quilometragem em Km'
    )
    combustivel = models.CharField(
        max_length=20,
        choices=CombustivelChoices.choices,
        default=CombustivelChoices.FLEX,
        verbose_name='Combustível'
    )
    cambio = models.CharField(
        max_length=20,
        choices=CambioChoices.choices,
        default=CambioChoices.MANUAL,
        verbose_name='Câmbio'
    )
    motor = models.CharField(
        max_length=30,
        verbose_name='Motor',
        help_text='Ex: 1.6 16V, 2.0 Turbo'
    )
    
    # Informações comerciais
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Preço',
        validators=[MinValueValidator(Decimal('1000.00'))]
    )
    condicao = models.CharField(
        max_length=10,
        choices=CondicaoChoices.choices,
        default=CondicaoChoices.SEMINOVO,
        verbose_name='Condição',
        db_index=True
    )
    destaque = models.BooleanField(
        default=False,
        verbose_name='Carro em Destaque',
        help_text='Aparece na página inicial'
    )
    
    # Descrição e imagens
    descricao = models.TextField(
        verbose_name='Descrição',
        help_text='Descrição detalhada do veículo'
    )
    imagem_principal = models.ImageField(
        upload_to='carros/',
        verbose_name='Imagem Principal'
    )
    imagem_2 = models.ImageField(
        upload_to='carros/',
        blank=True,
        null=True,
        verbose_name='Imagem 2'
    )
    imagem_3 = models.ImageField(
        upload_to='carros/',
        blank=True,
        null=True,
        verbose_name='Imagem 3'
    )
    imagem_4 = models.ImageField(
        upload_to='carros/',
        blank=True,
        null=True,
        verbose_name='Imagem 4'
    )
    
    class Meta:
        verbose_name = 'Carro'
        verbose_name_plural = 'Carros'
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['condicao', 'destaque']),
            models.Index(fields=['fabricante', 'condicao']),
            models.Index(fields=['preco']),
        ]
    
    def __str__(self) -> str:
        return f"{self.fabricante} {self.modelo} - {self.ano}"
    
    def get_absolute_url(self) -> str:
        """Retorna URL canônica do carro"""
        return reverse('core:detalhe_carro', kwargs={'pk': self.pk})
    
    @property
    def outras_imagens(self) -> List:
        """Retorna lista de imagens adicionais não vazias"""
        imagens = []
        for img_field in [self.imagem_2, self.imagem_3, self.imagem_4]:
            if img_field:
                imagens.append(img_field)
        return imagens
    
    @property
    def preco_formatado(self) -> str:
        """Retorna o preço formatado em reais brasileiros"""
        return f"R$ {self.preco:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    @property
    def quilometragem_formatada(self) -> str:
        """Retorna quilometragem formatada"""
        return f"{self.quilometragem:,} km".replace(',', '.')
    
    @property
    def descricao_resumida(self) -> str:
        """Retorna descrição truncada para listagens"""
        if len(self.descricao) <= 150:
            return self.descricao
        return self.descricao[:150] + '...'
    
    @property
    def is_disponivel(self) -> bool:
        """Verifica se o carro está disponível para venda"""
        return self.condicao in [self.CondicaoChoices.NOVO, self.CondicaoChoices.SEMINOVO]
    
    def save(self, *args, **kwargs):
        """Override do save para validações personalizadas"""
        # Garantir que fabricante e modelo sejam title case
        self.fabricante = self.fabricante.title()
        self.modelo = self.modelo.title()
        super().save(*args, **kwargs)


class ImagemSite(TimeStampedModel):
    """
    Gerencia imagens específicas do site
    Permite controle centralizado de assets visuais
    """
    
    class TipoChoices(models.TextChoices):
        CARRO_FLUTUANTE = 'carro_flutuante', 'Carro Flutuante'
        SOBRE_LOJA = 'sobre_loja', 'Imagem da Loja (Sobre)'
        BANNER_HOME = 'banner_home', 'Banner Principal'
        OUTRAS = 'outras', 'Outras Imagens'
    
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome da Imagem",
        help_text="Nome identificador da imagem"
    )
    tipo = models.CharField(
        max_length=20,
        choices=TipoChoices.choices,
        verbose_name="Tipo da Imagem",
        db_index=True
    )
    imagem = models.ImageField(
        upload_to='site_images/',
        verbose_name="Imagem"
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição",
        help_text="Descrição ou alt text da imagem"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Imagem visível no site"
    )
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem de Exibição"
    )
    
    class Meta:
        verbose_name = "Imagem do Site"
        verbose_name_plural = "Imagens do Site"
        ordering = ['tipo', 'ordem']
        indexes = [
            models.Index(fields=['tipo', 'ativo', 'ordem']),
        ]
    
    def __str__(self) -> str:
        return f"{self.nome} ({self.get_tipo_display()})"
