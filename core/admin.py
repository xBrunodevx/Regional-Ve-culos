from django.contrib import admin
from .models import Carro, Marca, ImagemSite


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativa', 'ordem']
    list_filter = ['ativa']
    search_fields = ['nome']
    list_editable = ['ativa', 'ordem']
    
    fieldsets = (
        ('Informações da Marca', {
            'fields': ('nome', 'logo', 'ativa', 'ordem')
        }),
    )


@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    list_display = ['fabricante', 'modelo', 'ano', 'preco', 'condicao', 'destaque', 'criado_em']
    list_filter = ['fabricante', 'condicao', 'destaque', 'ano']
    search_fields = ['modelo', 'fabricante', 'descricao']
    list_editable = ['destaque', 'condicao']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('modelo', 'fabricante', 'ano', 'cor')
        }),
        ('Detalhes Técnicos', {
            'fields': ('quilometragem', 'combustivel', 'cambio', 'motor')
        }),
        ('Informações Comerciais', {
            'fields': ('preco', 'condicao', 'destaque')
        }),
        ('Descrição e Imagens', {
            'fields': ('descricao', 'imagem_principal', 'imagem_2', 'imagem_3', 'imagem_4')
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ImagemSite)
class ImagemSiteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'ativo', 'ordem', 'data_criacao']
    list_filter = ['tipo', 'ativo', 'data_criacao']
    search_fields = ['nome', 'descricao']
    list_editable = ['ativo', 'ordem']
    readonly_fields = ['data_criacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'tipo', 'imagem', 'ativo')
        }),
        ('Detalhes', {
            'fields': ('descricao', 'ordem')
        }),
        ('Sistema', {
            'fields': ('data_criacao',),
            'classes': ('collapse',)
        }),
    )
