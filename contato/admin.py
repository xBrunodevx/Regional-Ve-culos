from django.contrib import admin
from .models import Lead, Financiamento


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'assunto', 'data_envio', 'respondido']
    list_filter = ['respondido', 'data_envio']
    search_fields = ['nome', 'email', 'assunto']
    list_editable = ['respondido']
    readonly_fields = ['data_envio']
    
    fieldsets = (
        ('Dados do Contato', {
            'fields': ('nome', 'email', 'telefone')
        }),
        ('Mensagem', {
            'fields': ('assunto', 'mensagem')
        }),
        ('Status', {
            'fields': ('respondido', 'data_envio')
        }),
    )


@admin.register(Financiamento)
class FinanciamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'renda_mensal', 'carro_interesse', 'data_solicitacao', 'aprovado', 'respondido']
    list_filter = ['aprovado', 'respondido', 'data_solicitacao']
    search_fields = ['nome', 'email', 'cpf']
    list_editable = ['aprovado', 'respondido']
    readonly_fields = ['data_solicitacao']
    
    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('nome', 'email', 'telefone', 'cpf')
        }),
        ('Dados Financeiros', {
            'fields': ('renda_mensal', 'profissao', 'entrada')
        }),
        ('Carro de Interesse', {
            'fields': ('carro_interesse', 'carro_texto')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Status', {
            'fields': ('aprovado', 'respondido', 'data_solicitacao')
        }),
    )
