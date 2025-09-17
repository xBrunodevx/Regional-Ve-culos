from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Lead, Financiamento
from .forms import LeadForm, FinanciamentoForm
from core.models import Carro


def contato(request):
    """View da página de contato"""
    if request.method == 'POST':
        print(f"Dados recebidos: {request.POST}")  # Debug
        form = LeadForm(request.POST)
        if form.is_valid():
            print("Formulário válido, salvando...")  # Debug
            lead = form.save()
            
            # Enviar email
            try:
                send_mail(
                    subject=f'Novo contato: {lead.assunto}',
                    message=f'''
                    Novo contato recebido:
                    
                    Nome: {lead.nome}
                    Email: {lead.email}
                    Telefone: {lead.telefone}
                    Assunto: {lead.assunto}
                    
                    Mensagem:
                    {lead.mensagem}
                    ''',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=['contato@regionalveiculos.com.br'],
                    fail_silently=True,
                )
                print("Email enviado com sucesso!")  # Debug
            except Exception as e:
                print(f"Erro ao enviar email: {e}")
            
            messages.success(request, 'Sua mensagem foi enviada com sucesso! Entraremos em contato em breve.')
            return redirect('contato:contato')
        else:
            print(f"Erros no formulário: {form.errors}")  # Debug
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = LeadForm()
    
    context = {
        'form': form,
    }
    return render(request, 'contato/contato.html', context)


def financiamento(request, carro_id=None):
    """View da página de financiamento"""
    carro = None
    if carro_id:
        carro = get_object_or_404(Carro, pk=carro_id)
    
    if request.method == 'POST':
        print(f"Dados recebidos: {request.POST}")  # Debug
        form = FinanciamentoForm(request.POST)
        if form.is_valid():
            print("Formulário de financiamento válido, salvando...")  # Debug
            financiamento = form.save(commit=False)
            if carro:
                financiamento.carro_interesse = carro
            
            financiamento.save()
            print("Financiamento salvo com sucesso!")  # Debug
            
            # Enviar email
            try:
                carro_info = carro or financiamento.carro_texto
                send_mail(
                    subject=f'Nova solicitação de financiamento - {financiamento.nome}',
                    message=f'''
                    Nova solicitação de financiamento:
                    
                    Nome: {financiamento.nome}
                    Email: {financiamento.email}
                    Telefone: {financiamento.telefone}
                    CPF: {financiamento.cpf}
                    
                    Dados Financeiros:
                    Renda Mensal: R$ {financiamento.renda_mensal}
                    Profissão: {financiamento.profissao}
                    Entrada: R$ {financiamento.entrada or '0.00'}
                    
                    Carro de Interesse: {carro_info}
                    
                    Observações:
                    {financiamento.observacoes}
                    ''',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=['financeiro@regionalveiculos.com.br'],
                    fail_silently=True,
                )
                print("Email de financiamento enviado!")  # Debug
            except Exception as e:
                print(f"Erro ao enviar email: {e}")
            
            messages.success(request, 'Sua solicitação de financiamento foi enviada! Analisaremos e entraremos em contato.')
            return redirect('core:estoque')
        else:
            print(f"Erros no formulário de financiamento: {form.errors}")  # Debug
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        initial_data = {}
        if carro:
            initial_data['carro_texto'] = f"{carro.fabricante} {carro.modelo} {carro.ano}"
        
        form = FinanciamentoForm(initial=initial_data)
    
    context = {
        'form': form,
        'carro': carro,
    }
    return render(request, 'contato/financiamento.html', context)
