// Regional Veículos - JavaScript Principal

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar navbar scroll
    initNavbarScroll();
    
    // Inicializar animações
    initAnimations();
    
    // Inicializar contadores animados
    initCounters();
    
    // Inicializar smooth scroll
    initSmoothScroll();
    
    // Inicializar formatação de campos
    initFieldFormatting();
    
    // Inicializar lazy loading para imagens
    initLazyLoading();
});

// Navbar transparente que fica vermelha no scroll
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) {
        console.log('Navbar não encontrada!');
        return;
    }
    
    console.log('Navbar scroll inicializado');
    
    function handleScroll() {
        const scrollY = window.scrollY;
        console.log('Scroll position:', scrollY);
        
        if (scrollY > 50) {
            navbar.classList.add('scrolled');
            console.log('Classe scrolled adicionada');
        } else {
            navbar.classList.remove('scrolled');
            console.log('Classe scrolled removida');
        }
    }
    
    // Verificar scroll inicial
    handleScroll();
    
    // Adicionar listener de scroll
    window.addEventListener('scroll', handleScroll);
}

// Animações de entrada
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('loading');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observar elementos para animação
    document.querySelectorAll('.car-card, .stat-item, .objective-item').forEach(el => {
        observer.observe(el);
    });
}

// Contadores animados
function initCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    const countUp = (element) => {
        const target = parseInt(element.getAttribute('data-target') || element.textContent);
        const duration = 2000; // 2 segundos
        const increment = target / (duration / 16); // 60fps
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target + '+';
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current) + '+';
            }
        }, 16);
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                countUp(entry.target);
                observer.unobserve(entry.target);
            }
        });
    });

    counters.forEach(counter => {
        observer.observe(counter);
    });
}

// Smooth scroll para links internos
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Formatação de campos
function initFieldFormatting() {
    // Formatação de telefone
    const phoneInputs = document.querySelectorAll('input[name="telefone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{2})(\d)/, '($1) $2');
            value = value.replace(/(\d{5})(\d)/, '$1-$2');
            e.target.value = value;
        });
    });

    // Formatação de CPF
    const cpfInputs = document.querySelectorAll('input[name="cpf"]');
    cpfInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            e.target.value = value;
        });
    });

    // Formatação de preço
    const priceInputs = document.querySelectorAll('input[name="renda_mensal"], input[name="entrada"]');
    priceInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = (value / 100).toFixed(2);
            value = value.replace('.', ',');
            value = value.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1.');
            e.target.value = 'R$ ' + value;
        });
    });
}

// Lazy loading para imagens
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// Carousel de marcas (auto-slide)
function initBrandsCarousel() {
    const carousel = document.querySelector('.brands-carousel .row');
    if (carousel) {
        let currentIndex = 0;
        const items = carousel.children;
        const totalItems = items.length;
        
        setInterval(() => {
            currentIndex = (currentIndex + 1) % totalItems;
            const offset = -currentIndex * (100 / 3); // Mostra 3 itens por vez
            carousel.style.transform = `translateX(${offset}%)`;
        }, 3000);
    }
}

// Modal de detalhes do carro
function showCarDetails(carId) {
    // Implementar modal com detalhes do carro
    fetch(`/api/carro/${carId}/`)
        .then(response => response.json())
        .then(data => {
            // Criar e mostrar modal com os dados
            createCarModal(data);
        })
        .catch(error => {
            console.error('Erro ao carregar detalhes do carro:', error);
        });
}

function createCarModal(carData) {
    const modalHTML = `
        <div class="modal fade" id="carModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${carData.fabricante} ${carData.modelo}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-6">
                                <img src="${carData.imagem_principal}" class="img-fluid rounded" alt="${carData.modelo}">
                            </div>
                            <div class="col-md-6">
                                <h4 class="text-danger">${carData.preco_formatado}</h4>
                                <ul class="list-unstyled">
                                    <li><strong>Ano:</strong> ${carData.ano}</li>
                                    <li><strong>Cor:</strong> ${carData.cor}</li>
                                    <li><strong>Km:</strong> ${carData.quilometragem.toLocaleString()}</li>
                                    <li><strong>Combustível:</strong> ${carData.combustivel}</li>
                                    <li><strong>Câmbio:</strong> ${carData.cambio}</li>
                                    <li><strong>Motor:</strong> ${carData.motor}</li>
                                </ul>
                                <p>${carData.descricao}</p>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <a href="https://wa.me/5511999999999?text=Tenho interesse no ${carData.fabricante} ${carData.modelo}" 
                           class="btn btn-success" target="_blank">
                            <i class="fab fa-whatsapp"></i> WhatsApp
                        </a>
                        <a href="/financiamento/${carData.id}/" class="btn btn-danger">
                            <i class="fas fa-calculator"></i> Financiar
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remover modal existente
    const existingModal = document.getElementById('carModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Adicionar novo modal
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('carModal'));
    modal.show();
}

// Filtros de estoque
function initStockFilters() {
    const filterForm = document.querySelector('.filter-form');
    if (filterForm) {
        const inputs = filterForm.querySelectorAll('input, select');
        
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                filterForm.submit();
            });
        });
    }
}

// Validação de formulários
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Função para scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Botão de voltar ao topo
function initScrollToTop() {
    const scrollButton = document.createElement('button');
    scrollButton.innerHTML = '<i class="fas fa-chevron-up"></i>';
    scrollButton.className = 'scroll-to-top';
    scrollButton.onclick = scrollToTop;
    
    document.body.appendChild(scrollButton);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollButton.classList.add('show');
        } else {
            scrollButton.classList.remove('show');
        }
    });
}

// Toast notifications
function showToast(message, type = 'success') {
    const toastHTML = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = toastContainer.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remover o toast do DOM após ser escondido
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// Inicializar funcionalidades específicas baseadas na página
function initPageSpecific() {
    const currentPage = document.body.getAttribute('data-page');
    
    switch(currentPage) {
        case 'estoque':
            initStockFilters();
            break;
        case 'contato':
        case 'financiamento':
            initFormValidation();
            break;
    }
}

// Chamar inicializações específicas da página
initPageSpecific();
