from django.db import models
from django.urls import reverse


class Marca(models.Model):
    """Modelo para representar marcas de carros"""
    nome = models.CharField(max_length=50, unique=True, verbose_name='Nome da Marca')
    logo = models.ImageField(upload_to='marcas/', verbose_name='Logo da Marca')
    ativa = models.BooleanField(default=True, verbose_name='Marca Ativa')
    ordem = models.IntegerField(default=0, verbose_name='Ordem de Exibição')
    
    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome


class Carro(models.Model):
    CONDICAO_CHOICES = [
        ('novo', 'Novo'),
        ('seminovo', 'Seminovo'),
        ('vendido', 'Vendido'),
    ]
    
    # Informações básicas
    modelo = models.CharField(max_length=100, verbose_name='Modelo')
    fabricante = models.CharField(max_length=50, verbose_name='Fabricante')
    ano = models.IntegerField(verbose_name='Ano')
    cor = models.CharField(max_length=30, verbose_name='Cor')
    
    # Detalhes técnicos
    quilometragem = models.IntegerField(verbose_name='Quilometragem')
    combustivel = models.CharField(max_length=20, default='Flex', verbose_name='Combustível')
    cambio = models.CharField(max_length=20, default='Manual', verbose_name='Câmbio')
    motor = models.CharField(max_length=30, verbose_name='Motor')
    
    # Informações comerciais
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    condicao = models.CharField(max_length=10, choices=CONDICAO_CHOICES, default='seminovo', verbose_name='Condição')
    destaque = models.BooleanField(default=False, verbose_name='Carro em Destaque')
    
    # Descrição e imagens
    descricao = models.TextField(verbose_name='Descrição')
    imagem_principal = models.ImageField(upload_to='carros/', verbose_name='Imagem Principal')
    imagem_2 = models.ImageField(upload_to='carros/', blank=True, null=True, verbose_name='Imagem 2')
    imagem_3 = models.ImageField(upload_to='carros/', blank=True, null=True, verbose_name='Imagem 3')
    imagem_4 = models.ImageField(upload_to='carros/', blank=True, null=True, verbose_name='Imagem 4')
    
    # Metadados
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Carro'
        verbose_name_plural = 'Carros'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.fabricante} {self.modelo} - {self.ano}"
    
    def get_absolute_url(self):
        return reverse('core:detalhe_carro', kwargs={'pk': self.pk})
    
    def get_outras_imagens(self):
        """Retorna lista de imagens adicionais não vazias"""
        imagens = []
        for img in [self.imagem_2, self.imagem_3, self.imagem_4]:
            if img:
                imagens.append(img)
        return imagens
    
    def get_preco_formatado(self):
        """Retorna o preço formatado em reais"""
        return f"R$ {self.preco:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


class ImagemSite(models.Model):
    """Modelo para imagens específicas do site"""
    TIPO_CHOICES = [
        ('carro_flutuante', 'Carro Flutuante'),
        ('sobre_loja', 'Imagem da Loja (Sobre)'),
        ('banner_home', 'Banner Principal'),
        ('outras', 'Outras Imagens'),
    ]
    
    nome = models.CharField(max_length=100, verbose_name="Nome da Imagem")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo da Imagem")
    imagem = models.ImageField(upload_to='site_images/', verbose_name="Imagem")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    ordem = models.IntegerField(default=0, verbose_name="Ordem de Exibição")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    
    class Meta:
        verbose_name = "Imagem do Site"
        verbose_name_plural = "Imagens do Site"
        ordering = ['tipo', 'ordem']
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"
