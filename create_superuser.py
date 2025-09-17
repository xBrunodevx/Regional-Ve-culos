#!/usr/bin/env python
"""
Script para criar superusuário automaticamente
"""
import os
import django
from django.conf import settings
from django.contrib.auth import get_user_model

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'regional_veiculos.settings')
django.setup()

User = get_user_model()

# Dados do superusuário
username = 'admin'
email = 'admin@regionalveiculos.com'
password = 'Admin@2024!'

# Verificar se o usuário já existe
if User.objects.filter(username=username).exists():
    print(f'✅ Superusuário "{username}" já existe!')
else:
    # Criar superusuário
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f'✅ Superusuário "{username}" criado com sucesso!')
    print(f'📧 Email: {email}')
    print(f'🔑 Senha: {password}')
