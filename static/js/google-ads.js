// Google Ads e Remarketing Configuration
// Regional Veículos - Configuração de Campanhas e Conversões

// Google Ads Conversion Tracking
function setupGoogleAdsConversions() {
    // Conversion 1: Contact Form Submission
    window.addEventListener('load', function() {
        // Track contact form submissions
        document.querySelectorAll('form[data-track="contact"]').forEach(form => {
            form.addEventListener('submit', function() {
                gtag('event', 'conversion', {
                    'send_to': 'AW-XXXXXXXXX/contact_conversion',
                    'value': 100.0,
                    'currency': 'BRL'
                });
            });
        });
        
        // Track financing form submissions
        document.querySelectorAll('form[data-track="financing"]').forEach(form => {
            form.addEventListener('submit', function() {
                const carPrice = this.dataset.carPrice || 50000;
                gtag('event', 'conversion', {
                    'send_to': 'AW-XXXXXXXXX/financing_conversion',
                    'value': parseFloat(carPrice) * 0.1, // 10% do valor do carro como valor da conversão
                    'currency': 'BRL'
                });
            });
        });
        
        // Track phone clicks
        document.querySelectorAll('a[href^="tel:"]').forEach(link => {
            link.addEventListener('click', function() {
                gtag('event', 'conversion', {
                    'send_to': 'AW-XXXXXXXXX/phone_call_conversion',
                    'value': 50.0,
                    'currency': 'BRL'
                });
            });
        });
        
        // Track WhatsApp clicks
        document.querySelectorAll('a[href*="wa.me"], a[href*="whatsapp.com"]').forEach(link => {
            link.addEventListener('click', function() {
                gtag('event', 'conversion', {
                    'send_to': 'AW-XXXXXXXXX/whatsapp_conversion',
                    'value': 30.0,
                    'currency': 'BRL'
                });
            });
        });
    });
}

// Enhanced Ecommerce para Google Ads
function setupEnhancedEcommerce() {
    // Track product views (carros)
    window.trackCarView = function(carData) {
        gtag('event', 'view_item', {
            'currency': 'BRL',
            'value': parseFloat(carData.price),
            'items': [{
                'item_id': carData.id,
                'item_name': `${carData.brand} ${carData.model} ${carData.year}`,
                'item_category': 'Carros Seminovos',
                'item_brand': carData.brand,
                'price': parseFloat(carData.price),
                'quantity': 1
            }]
        });
    };
    
    // Track when user shows interest (financing/contact)
    window.trackCarInterest = function(carData, action) {
        gtag('event', 'add_to_cart', {
            'currency': 'BRL',
            'value': parseFloat(carData.price),
            'items': [{
                'item_id': carData.id,
                'item_name': `${carData.brand} ${carData.model} ${carData.year}`,
                'item_category': 'Carros Seminovos',
                'item_brand': carData.brand,
                'price': parseFloat(carData.price),
                'quantity': 1
            }]
        });
    };
    
    // Track financing start
    window.trackFinancingStart = function(carData) {
        gtag('event', 'begin_checkout', {
            'currency': 'BRL',
            'value': parseFloat(carData.price),
            'items': [{
                'item_id': carData.id,
                'item_name': `${carData.brand} ${carData.model} ${carData.year}`,
                'item_category': 'Carros Seminovos',
                'item_brand': carData.brand,
                'price': parseFloat(carData.price),
                'quantity': 1
            }]
        });
    };
}

// Remarketing Lists for Search Ads (RLSA)
function setupRemarketingLists() {
    // List 1: Visitors who viewed cars
    gtag('config', 'AW-XXXXXXXXX', {
        'custom_map': {
            'custom_parameter_1': 'car_viewer'
        }
    });
    
    // List 2: Visitors who started financing process
    if (window.location.pathname.includes('/financiamento/')) {
        gtag('event', 'page_view', {
            'custom_parameter_1': 'financing_interested'
        });
    }
    
    // List 3: Visitors who contacted us
    window.addEventListener('load', function() {
        document.querySelectorAll('[data-track="contact"]').forEach(element => {
            element.addEventListener('click', function() {
                gtag('event', 'page_view', {
                    'custom_parameter_1': 'contact_initiated'
                });
            });
        });
    });
}

// Dynamic Remarketing (Produtos dinâmicos)
function setupDynamicRemarketing() {
    // Para páginas de carros individuais
    if (window.location.pathname.includes('/carro/')) {
        const carData = document.querySelector('[data-car-info]');
        if (carData) {
            gtag('event', 'page_view', {
                'send_to': 'AW-XXXXXXXXX',
                'ecomm_prodid': carData.dataset.carId,
                'ecomm_pagetype': 'product',
                'ecomm_totalvalue': parseFloat(carData.dataset.carPrice)
            });
        }
    }
    
    // Para página de estoque
    if (window.location.pathname.includes('/estoque/')) {
        gtag('event', 'page_view', {
            'send_to': 'AW-XXXXXXXXX',
            'ecomm_pagetype': 'category'
        });
    }
    
    // Para página inicial
    if (window.location.pathname === '/') {
        gtag('event', 'page_view', {
            'send_to': 'AW-XXXXXXXXX',
            'ecomm_pagetype': 'home'
        });
    }
}

// Inicializar todas as configurações
document.addEventListener('DOMContentLoaded', function() {
    setupGoogleAdsConversions();
    setupEnhancedEcommerce();
    setupRemarketingLists();
    setupDynamicRemarketing();
    
    console.log('[Google Ads] Configurações carregadas');
});
