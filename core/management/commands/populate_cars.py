from django.core.management.base import BaseCommand
from core.models import Carro, Marca


class Command(BaseCommand):
    help = 'Popula o banco de dados com carros e marcas'

    def handle(self, *args, **options):
        self.stdout.write('Criando marcas...')
        
        # Criar marcas se não existirem
        marcas_data = [
            {'nome': 'BMW', 'ordem': 1},
            {'nome': 'Ford', 'ordem': 2},
            {'nome': 'Volkswagen', 'ordem': 3},
            {'nome': 'Toyota', 'ordem': 4},
            {'nome': 'Honda', 'ordem': 5},
        ]
        
        for marca_info in marcas_data:
            marca, created = Marca.objects.get_or_create(
                nome=marca_info['nome'],
                defaults={
                    'ordem': marca_info['ordem'],
                    'ativa': True,
                    'logo': f'marcas/{marca_info["nome"].lower()}.png'
                }
            )
            if created:
                self.stdout.write(f'Marca {marca.nome} criada')

        # Dados dos carros
        carros_data = [
            {
                'modelo': 'Z4 sDrive30i',
                'fabricante': 'BMW',
                'ano': 2023,
                'cor': 'Azul Metálico',
                'quilometragem': 5000,
                'combustivel': 'Gasolina',
                'cambio': 'Automático',
                'motor': '2.0 Turbo',
                'preco': 450000.00,
                'condicao': 'seminovo',
                'destaque': True,
                'descricao': 'BMW Z4 sDrive30i em excelente estado, com apenas 5.000 km rodados. Motor 2.0 turbo, câmbio automático, cor azul metálico. Carro esportivo premium.'
            },
            {
                'modelo': 'Territory Titanium 1.5',
                'fabricante': 'Ford',
                'ano': 2022,
                'cor': 'Branco Pérola',
                'quilometragem': 15000,
                'combustivel': 'Flex',
                'cambio': 'Automático',
                'motor': '1.5 EcoBoost',
                'preco': 180000.00,
                'condicao': 'seminovo',
                'destaque': True,
                'descricao': 'Ford Territory Titanium com motor 1.5 EcoBoost, câmbio automático CVT, cor branco pérola. SUV moderno e econômico.'
            },
            {
                'modelo': 'Virtus Highline 1.0',
                'fabricante': 'Volkswagen',
                'ano': 2024,
                'cor': 'Prata',
                'quilometragem': 2000,
                'combustivel': 'Flex',
                'cambio': 'Automático',
                'motor': '1.0 TSI',
                'preco': 95000.00,
                'condicao': 'seminovo',
                'destaque': True,
                'descricao': 'Volkswagen Virtus Highline 1.0 TSI, praticamente zero km. Sedã compacto com tecnologia avançada e ótimo consumo.'
            },
            {
                'modelo': 'Camry XLE Hybrid',
                'fabricante': 'Toyota',
                'ano': 2023,
                'cor': 'Preto',
                'quilometragem': 8000,
                'combustivel': 'Híbrido',
                'cambio': 'Automático',
                'motor': '2.5 Hybrid',
                'preco': 280000.00,
                'condicao': 'seminovo',
                'destaque': False,
                'descricao': 'Toyota Camry XLE Hybrid, sedã premium com motorização híbrida. Excelente economia de combustível e conforto superior.'
            },
            {
                'modelo': 'City EX 1.5',
                'fabricante': 'Honda',
                'ano': 2023,
                'cor': 'Cinza Metálico',
                'quilometragem': 12000,
                'combustivel': 'Flex',
                'cambio': 'CVT',
                'motor': '1.5 i-VTEC',
                'preco': 105000.00,
                'condicao': 'seminovo',
                'destaque': False,
                'descricao': 'Honda City EX 1.5 i-VTEC com câmbio CVT. Sedã confortável e econômico, ideal para o dia a dia.'
            },
            {
                'modelo': 'i3 BEV 120Ah',
                'fabricante': 'BMW',
                'ano': 2022,
                'cor': 'Branco',
                'quilometragem': 18000,
                'combustivel': 'Elétrico',
                'cambio': 'Automático',
                'motor': 'Elétrico 170cv',
                'preco': 220000.00,
                'condicao': 'seminovo',
                'destaque': False,
                'descricao': 'BMW i3 totalmente elétrico, autonomia de 300km. Carro sustentável com design futurista e tecnologia de ponta.'
            },
            {
                'modelo': 'Maverick Lariat FX4',
                'fabricante': 'Ford',
                'ano': 2023,
                'cor': 'Vermelho',
                'quilometragem': 7000,
                'combustivel': 'Gasolina',
                'cambio': 'Automático',
                'motor': '2.0 EcoBoost',
                'preco': 320000.00,
                'condicao': 'seminovo',
                'destaque': False,
                'descricao': 'Ford Maverick Lariat FX4, picape compacta com motor 2.0 EcoBoost. Versatilidade e potência em um só veículo.'
            },
            {
                'modelo': 'Nivus Highline 1.0',
                'fabricante': 'Volkswagen',
                'ano': 2023,
                'cor': 'Azul Escuro',
                'quilometragem': 10000,
                'combustivel': 'Flex',
                'cambio': 'Automático',
                'motor': '1.0 TSI',
                'preco': 98000.00,
                'condicao': 'seminovo',
                'destaque': False,
                'descricao': 'Volkswagen Nivus Highline 1.0 TSI, SUV coupé moderno com design arrojado e tecnologia conectada.'
            },
            {
                'modelo': 'SW4 SRX 2.8',
                'fabricante': 'Toyota',
                'ano': 2022,
                'cor': 'Prata Metálico',
                'quilometragem': 25000,
                'combustivel': 'Diesel',
                'cambio': 'Automático',
                'motor': '2.8 Turbo Diesel',
                'preco': 380000.00,
                'condicao': 'seminovo',
                'destaque': False,
                'descricao': 'Toyota SW4 SRX 2.8 Turbo Diesel, SUV robusto para aventuras. Tração 4x4, 7 lugares e grande capacidade off-road.'
            },
            {
                'modelo': 'WR-V EXL 1.5',
                'fabricante': 'Honda',
                'ano': 2023,
                'cor': 'Laranja',
                'quilometragem': 6000,
                'combustivel': 'Flex',
                'cambio': 'CVT',
                'motor': '1.5 i-VTEC',
                'preco': 110000.00,
                'condicao': 'seminovo',
                'destaque': False,
                'descricao': 'Honda WR-V EXL 1.5 i-VTEC, SUV compacto com design jovem e moderno. Ótimo custo-benefício.'
            },
            {
                'modelo': 'X5 xDrive45e',
                'fabricante': 'BMW',
                'ano': 2023,
                'cor': 'Preto Metálico',
                'quilometragem': 3000,
                'combustivel': 'Híbrido',
                'cambio': 'Automático',
                'motor': '3.0 Híbrido',
                'preco': 650000.00,
                'condicao': 'seminovo',
                'destaque': False,
                'descricao': 'BMW X5 xDrive45e, SUV premium híbrido plug-in. Luxo, performance e eficiência energética em um só veículo.'
            },
            {
                'modelo': 'Fusion Titanium Hybrid',
                'fabricante': 'Ford',
                'ano': 2022,
                'cor': 'Cinza Escuro',
                'quilometragem': 20000,
                'combustivel': 'Híbrido',
                'cambio': 'Automático',
                'motor': '2.0 Hybrid',
                'preco': 140000.00,
                'condicao': 'seminovo',
                'destaque': False,
                'descricao': 'Ford Fusion Titanium Hybrid, sedã premium com motorização híbrida. Economia e conforto excepcionais.'
            }
        ]

        self.stdout.write('Criando carros...')
        
        for carro_data in carros_data:
            carro, created = Carro.objects.get_or_create(
                modelo=carro_data['modelo'],
                fabricante=carro_data['fabricante'],
                ano=carro_data['ano'],
                defaults=carro_data
            )
            
            if created:
                self.stdout.write(f'Carro {carro.fabricante} {carro.modelo} criado')
            else:
                self.stdout.write(f'Carro {carro.fabricante} {carro.modelo} já existe')

        # Estatísticas
        total_carros = Carro.objects.count()
        carros_destaque = Carro.objects.filter(destaque=True).count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nConcluído!\n'
                f'Total de carros: {total_carros}\n'
                f'Carros em destaque: {carros_destaque}\n'
                f'Configuração: 6 carros por página, 3 em destaque'
            )
        )
