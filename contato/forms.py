from django import forms
from decimal import Decimal, InvalidOperation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Lead, Financiamento
from core.models import Carro


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['nome', 'email', 'telefone', 'assunto', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu nome completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seu.email@exemplo.com'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'assunto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Assunto da mensagem'
            }),
            'mensagem': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Digite sua mensagem aqui...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('telefone', css_class='form-group col-md-6 mb-3'),
                Column('assunto', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'mensagem',
            Submit('submit', 'Enviar Mensagem', css_class='btn btn-danger btn-lg')
        )


class FinanciamentoForm(forms.ModelForm):
    # Sobrescrever campos monetários para aceitar formato brasileiro
    renda_mensal = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control money-input',
            'placeholder': 'R$ 0,00',
            'data-mask': 'money'
        }),
        help_text='Informe sua renda mensal bruta'
    )
    
    entrada = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control money-input',
            'placeholder': 'R$ 0,00',
            'data-mask': 'money'
        }),
        help_text='Valor de entrada (opcional)'
    )
    
    class Meta:
        model = Financiamento
        fields = [
            'nome', 'email', 'telefone', 'cpf',
            'renda_mensal', 'profissao', 'entrada',
            'carro_interesse', 'carro_texto', 'observacoes'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seu.email@exemplo.com'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00'
            }),
            'profissao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sua profissão'
            }),
            'carro_interesse': forms.Select(attrs={
                'class': 'form-control'
            }),
            'carro_texto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Toyota Corolla 2020'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observações adicionais...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('telefone', css_class='form-group col-md-6 mb-3'),
                Column('cpf', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('renda_mensal', css_class='form-group col-md-6 mb-3'),
                Column('profissao', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('entrada', css_class='form-group col-md-6 mb-3'),
                Column('carro_interesse', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'carro_texto',
            'observacoes',
            Submit('submit', 'Solicitar Financiamento', css_class='btn btn-danger btn-lg')
        )

    def clean_renda_mensal(self):
        """Limpar e converter valor da renda mensal"""
        renda = self.cleaned_data.get('renda_mensal')
        
        if not renda:
            raise forms.ValidationError('Renda mensal é obrigatória.')
            
        # Remove R$, espaços, pontos e substitui vírgula por ponto
        renda_str = str(renda).replace('R$', '').replace(' ', '').strip()
        
        # Se estiver vazio após limpeza, erro
        if not renda_str:
            raise forms.ValidationError('Digite um valor válido para a renda mensal.')
            
        # Remove pontos (separadores de milhares) e substitui vírgula por ponto
        renda_str = renda_str.replace('.', '').replace(',', '.')
        
        try:
            valor_decimal = Decimal(renda_str)
            if valor_decimal <= 0:
                raise forms.ValidationError('A renda mensal deve ser maior que zero.')
            return valor_decimal
        except (ValueError, InvalidOperation) as e:
            raise forms.ValidationError('Digite um valor válido para a renda mensal (ex: R$ 5.000,00).')

    def clean_entrada(self):
        """Limpar e converter valor da entrada"""
        entrada = self.cleaned_data.get('entrada')
        
        # Entrada é opcional
        if not entrada:
            return None
            
        # Remove R$, espaços, pontos e substitui vírgula por ponto
        entrada_str = str(entrada).replace('R$', '').replace(' ', '').strip()
        
        # Se estiver vazio após limpeza, retorna None
        if not entrada_str:
            return None
            
        # Remove pontos (separadores de milhares) e substitui vírgula por ponto
        entrada_str = entrada_str.replace('.', '').replace(',', '.')
        
        try:
            valor_decimal = Decimal(entrada_str)
            if valor_decimal < 0:
                raise forms.ValidationError('O valor de entrada não pode ser negativo.')
            return valor_decimal
        except (ValueError, InvalidOperation) as e:
            raise forms.ValidationError('Digite um valor válido para a entrada (ex: R$ 10.000,00).')

    def clean(self):
        """Validação geral do formulário"""
        cleaned_data = super().clean()
        
        # Verificar se pelo menos um campo de carro foi preenchido (temporariamente desabilitado)
        # carro_interesse = cleaned_data.get('carro_interesse')
        # carro_texto = cleaned_data.get('carro_texto', '').strip()
        
        # if not carro_interesse and not carro_texto:
        #     raise forms.ValidationError('Por favor, selecione um carro ou descreva o carro de interesse.')
        
        return cleaned_data

    def clean_cpf(self):
        """Validação básica do CPF"""
        cpf = self.cleaned_data.get('cpf')
        if not cpf:
            raise forms.ValidationError('CPF é obrigatório.')
        
        # Remove caracteres não numéricos
        cpf_numeros = ''.join(filter(str.isdigit, cpf))
        
        # Verifica se tem 11 dígitos
        if len(cpf_numeros) != 11:
            raise forms.ValidationError('CPF deve ter 11 dígitos.')
            
        return cpf
