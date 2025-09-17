from django.db import models
from core.models import Carro


class Lead(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    email = models.EmailField(verbose_name='E-mail')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    assunto = models.CharField(max_length=100, verbose_name='Assunto')
    mensagem = models.TextField(verbose_name='Mensagem')
    data_envio = models.DateTimeField(auto_now_add=True)
    respondido = models.BooleanField(default=False, verbose_name='Respondido')
    
    class Meta:
        verbose_name = 'Lead de Contato'
        verbose_name_plural = 'Leads de Contato'
        ordering = ['-data_envio']
    
    def __str__(self):
        return f"{self.nome} - {self.assunto}"


class Financiamento(models.Model):
    # Dados pessoais
    nome = models.CharField(max_length=100, verbose_name='Nome Completo')
    email = models.EmailField(verbose_name='E-mail')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    cpf = models.CharField(max_length=14, verbose_name='CPF')
    
    # Dados financeiros
    renda_mensal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Renda Mensal')
    profissao = models.CharField(max_length=100, verbose_name='Profissão')
    entrada = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Valor de Entrada')
    
    # Carro de interesse
    carro_interesse = models.ForeignKey(Carro, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Carro de Interesse')
    carro_texto = models.CharField(max_length=200, blank=True, verbose_name='Carro (se não listado)')
    
    # Observações
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    
    # Metadados
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    aprovado = models.BooleanField(default=False, verbose_name='Pré-aprovado')
    respondido = models.BooleanField(default=False, verbose_name='Respondido')
    
    class Meta:
        verbose_name = 'Solicitação de Financiamento'
        verbose_name_plural = 'Solicitações de Financiamento'
        ordering = ['-data_solicitacao']
    
    def __str__(self):
        carro = self.carro_interesse or self.carro_texto
        return f"{self.nome} - {carro}"
