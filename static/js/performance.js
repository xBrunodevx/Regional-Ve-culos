// Performance Optimization - Core Web Vitals
// Regional Veículos - Otimização de Performance

(function() {
    'use strict';
    
    // Lazy Loading de Imagens Avançado
    function setupLazyLoading() {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    
                    // Preload da imagem
                    const imageLoader = new Image();
                    imageLoader.onload = () => {
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        img.classList.add('loaded');
                    };
                    imageLoader.src = img.dataset.src;
                    
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.1
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Preload de recursos críticos
    function preloadCriticalResources() {
        const criticalImages = [
            '/static/images/imagemcarr.jpg', // Banner principal
            '/static/images/logo-regional-veiculos.png' // Logo
        ];
        
        criticalImages.forEach(src => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'image';
            link.href = src;
            document.head.appendChild(link);
        });
    }
    
    // Otimização de fontes
    function optimizeFonts() {
        // Preload Google Fonts
        const fontLink = document.createElement('link');
        fontLink.rel = 'preload';
        fontLink.as = 'style';
        fontLink.href = 'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap';
        fontLink.onload = function() {
            this.onload = null;
            this.rel = 'stylesheet';
        };
        document.head.appendChild(fontLink);
    }
    
    // Compressão de imagens dinamicamente
    function setupImageCompression() {
        const images = document.querySelectorAll('img[data-compress]');
        
        images.forEach(img => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            img.onload = function() {
                const maxWidth = parseInt(img.dataset.maxWidth) || 800;
                const quality = parseFloat(img.dataset.quality) || 0.8;
                
                // Redimensionar se necessário
                let { width, height } = img;
                if (width > maxWidth) {
                    height = (height * maxWidth) / width;
                    width = maxWidth;
                }
                
                canvas.width = width;
                canvas.height = height;
                
                ctx.drawImage(img, 0, 0, width, height);
                
                // Converter para WebP se suportado
                const format = supportsWebP() ? 'image/webp' : 'image/jpeg';
                const compressedDataUrl = canvas.toDataURL(format, quality);
                
                img.src = compressedDataUrl;
            };
        });
    }
    
    // Verificar suporte a WebP
    function supportsWebP() {
        const canvas = document.createElement('canvas');
        canvas.width = 1;
        canvas.height = 1;
        return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
    }
    
    // Cache Service Worker
    function setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/js/sw.js')
                .then(registration => {
                    console.log('[SW] Registrado com sucesso:', registration);
                })
                .catch(error => {
                    console.log('[SW] Falha no registro:', error);
                });
        }
    }
    
    // Métricas Core Web Vitals
    function measureCoreWebVitals() {
        // Largest Contentful Paint (LCP)
        new PerformanceObserver(entryList => {
            const entries = entryList.getEntries();
            const lastEntry = entries[entries.length - 1];
            
            // Enviar para Analytics
            gtag('event', 'web_vitals', {
                metric_name: 'LCP',
                metric_value: Math.round(lastEntry.startTime),
                metric_rating: lastEntry.startTime < 2500 ? 'good' : lastEntry.startTime < 4000 ? 'needs-improvement' : 'poor'
            });
        }).observe({ entryTypes: ['largest-contentful-paint'] });
        
        // First Input Delay (FID)
        new PerformanceObserver(entryList => {
            const firstInput = entryList.getEntries()[0];
            
            gtag('event', 'web_vitals', {
                metric_name: 'FID',
                metric_value: Math.round(firstInput.processingStart - firstInput.startTime),
                metric_rating: firstInput.processingStart - firstInput.startTime < 100 ? 'good' : firstInput.processingStart - firstInput.startTime < 300 ? 'needs-improvement' : 'poor'
            });
        }).observe({ entryTypes: ['first-input'] });
        
        // Cumulative Layout Shift (CLS)
        let clsValue = 0;
        let clsEntries = [];
        
        new PerformanceObserver(entryList => {
            for (const entry of entryList.getEntries()) {
                if (!entry.hadRecentInput) {
                    const firstSessionEntry = clsEntries[0];
                    const lastSessionEntry = clsEntries[clsEntries.length - 1];
                    
                    if (!firstSessionEntry || 
                        entry.startTime - lastSessionEntry.startTime > 1000 ||
                        entry.startTime - firstSessionEntry.startTime > 5000) {
                        clsEntries = [entry];
                    } else {
                        clsEntries.push(entry);
                    }
                    
                    clsValue = clsEntries.reduce((sum, entry) => sum + entry.value, 0);
                }
            }
        }).observe({ entryTypes: ['layout-shift'] });
        
        // Enviar CLS no final da sessão
        window.addEventListener('beforeunload', () => {
            gtag('event', 'web_vitals', {
                metric_name: 'CLS',
                metric_value: Math.round(clsValue * 1000),
                metric_rating: clsValue < 0.1 ? 'good' : clsValue < 0.25 ? 'needs-improvement' : 'poor'
            });
        });
    }
    
    // Defer de scripts não críticos
    function deferNonCriticalScripts() {
        const scripts = document.querySelectorAll('script[data-defer]');
        
        scripts.forEach(script => {
            const newScript = document.createElement('script');
            newScript.src = script.src;
            newScript.defer = true;
            
            // Adicionar após o load da página
            window.addEventListener('load', () => {
                document.head.appendChild(newScript);
            });
        });
    }
    
    // Inicialização
    document.addEventListener('DOMContentLoaded', function() {
        setupLazyLoading();
        preloadCriticalResources();
        optimizeFonts();
        setupImageCompression();
        deferNonCriticalScripts();
        
        console.log('[Performance] Otimizações carregadas');
    });
    
    window.addEventListener('load', function() {
        setupServiceWorker();
        measureCoreWebVitals();
        
        console.log('[Performance] Métricas inicializadas');
    });
    
})();
