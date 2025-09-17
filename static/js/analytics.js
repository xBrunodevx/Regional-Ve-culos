// Google Analytics 4 e Tag Manager - Event Tracking
// Regional Veículos - Analytics e Conversões

(function() {
    'use strict';
    
    // Configuração de debugging
    const DEBUG_MODE = true;
    const log = (...args) => DEBUG_MODE && console.log('[GA4 Tracking]', ...args);
    
    // Função auxiliar para envio de eventos
    function trackEvent(eventName, parameters = {}) {
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, parameters);
            log(`Evento enviado: ${eventName}`, parameters);
        }
        
        // Também enviar para Tag Manager se disponível
        if (typeof dataLayer !== 'undefined') {
            dataLayer.push({
                event: eventName,
                ...parameters
            });
        }
    }
    
    // Função para tracking de visualização de carro
    function trackCarView(carId, carBrand, carModel, carYear, carPrice) {
        trackEvent('view_item', {
            currency: 'BRL',
            value: parseFloat(carPrice),
            item_category: 'Carros Seminovos',
            item_brand: carBrand,
            item_name: `${carBrand} ${carModel} ${carYear}`,
            item_id: carId
        });
    }
    
    // Função para tracking de leads/contatos
    function trackLead(leadType, carId = null) {
        const parameters = {
            currency: 'BRL',
            value: 100.00, // Valor estimado do lead
            lead_type: leadType
        };
        
        if (carId) {
            parameters.item_id = carId;
        }
        
        trackEvent('generate_lead', parameters);
    }
    
    // Função para tracking de início de financiamento
    function trackFinancingStart(carId = null, carPrice = null) {
        const parameters = {
            currency: 'BRL'
        };
        
        if (carPrice) {
            parameters.value = parseFloat(carPrice);
        }
        
        if (carId) {
            parameters.item_id = carId;
        }
        
        trackEvent('begin_checkout', parameters);
    }
    
    // Auto-tracking quando DOM estiver pronto
    document.addEventListener('DOMContentLoaded', function() {
        log('Analytics tracking iniciado');
        
        // Track visualização de página de carro individual
        if (window.location.pathname.includes('/carro/')) {
            const carData = document.querySelector('[data-car-info]');
            if (carData) {
                const carId = carData.dataset.carId;
                const carBrand = carData.dataset.carBrand;
                const carModel = carData.dataset.carModel;
                const carYear = carData.dataset.carYear;
                const carPrice = carData.dataset.carPrice;
                
                trackCarView(carId, carBrand, carModel, carYear, carPrice);
            }
        }
        
        // Track cliques em botões de contato
        document.querySelectorAll('[data-track="contact"]').forEach(element => {
            element.addEventListener('click', function() {
                const contactType = this.dataset.contactType || 'generic';
                const carId = this.dataset.carId || null;
                trackLead(contactType, carId);
            });
        });
        
        // Track cliques em WhatsApp
        document.querySelectorAll('a[href*="wa.me"], a[href*="whatsapp.com"]').forEach(element => {
            element.addEventListener('click', function() {
                trackEvent('contact', {
                    method: 'whatsapp',
                    content_type: 'link'
                });
            });
        });
        
        // Track cliques em telefone
        document.querySelectorAll('a[href^="tel:"]').forEach(element => {
            element.addEventListener('click', function() {
                trackEvent('contact', {
                    method: 'phone',
                    content_type: 'link'
                });
            });
        });
        
        // Track cliques em email
        document.querySelectorAll('a[href^="mailto:"]').forEach(element => {
            element.addEventListener('click', function() {
                trackEvent('contact', {
                    method: 'email',
                    content_type: 'link'
                });
            });
        });
        
        // Track submissão de formulários
        document.querySelectorAll('form[data-track="form"]').forEach(form => {
            form.addEventListener('submit', function() {
                const formType = this.dataset.formType || 'generic';
                const carId = this.dataset.carId || null;
                
                if (formType === 'financing') {
                    const carPrice = this.dataset.carPrice || null;
                    trackFinancingStart(carId, carPrice);
                } else {
                    trackLead(formType, carId);
                }
            });
        });
        
        // Track scroll depth (25%, 50%, 75%, 100%)
        let scrollDepths = [25, 50, 75, 100];
        let trackedDepths = [];
        
        window.addEventListener('scroll', function() {
            const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
            
            scrollDepths.forEach(depth => {
                if (scrollPercent >= depth && !trackedDepths.includes(depth)) {
                    trackedDepths.push(depth);
                    trackEvent('scroll', {
                        scroll_depth: depth
                    });
                }
            });
        });
        
        // Track tempo na página (engagement)
        let pageStartTime = Date.now();
        let engagementSent = false;
        
        // Enviar evento de engagement após 30 segundos
        setTimeout(() => {
            if (!engagementSent) {
                trackEvent('page_engagement', {
                    engagement_time_msec: 30000
                });
                engagementSent = true;
            }
        }, 30000);
        
        // Track saída da página
        window.addEventListener('beforeunload', function() {
            const timeOnPage = Date.now() - pageStartTime;
            
            if (timeOnPage > 10000 && !engagementSent) { // Mais de 10 segundos
                trackEvent('page_engagement', {
                    engagement_time_msec: timeOnPage
                });
            }
        });
        
        log('Event listeners configurados');
    });
    
    // Expor funções globalmente para uso manual
    window.regionalAnalytics = {
        trackCarView,
        trackLead,
        trackFinancingStart,
        trackEvent
    };
    
    log('Regional Analytics carregado');
})();
