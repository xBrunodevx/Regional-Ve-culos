/**
 * Regional Veículos - Main JavaScript Module
 * Professional implementation following ES6+ standards
 * @version 2.0.0
 * @author Regional Veículos Development Team
 */

(function() {
    'use strict';

    /**
     * Application Configuration
     */
    const APP_CONFIG = {
        animation: {
            typewriterSpeed: 100,
            fadeInDuration: 300,
            slideInDuration: 500
        },
        ui: {
            navbarOffset: 100,
            scrollThreshold: 50,
            mobileBreakpoint: 768
        },
        performance: {
            debounceDelay: 250,
            throttleDelay: 100
        }
    };

    /**
     * Utility Functions
     */
    const Utils = {
        /**
         * Debounce function execution
         * @param {Function} func - Function to debounce
         * @param {number} wait - Wait time in milliseconds
         * @param {boolean} immediate - Execute immediately
         * @returns {Function} Debounced function
         */
        debounce(func, wait, immediate = false) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    timeout = null;
                    if (!immediate) func.apply(this, args);
                };
                const callNow = immediate && !timeout;
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
                if (callNow) func.apply(this, args);
            };
        },

        /**
         * Throttle function execution
         * @param {Function} func - Function to throttle
         * @param {number} limit - Time limit in milliseconds
         * @returns {Function} Throttled function
         */
        throttle(func, limit) {
            let inThrottle;
            return function executedFunction(...args) {
                if (!inThrottle) {
                    func.apply(this, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        },

        /**
         * Check if element is in viewport
         * @param {HTMLElement} element - Element to check
         * @returns {boolean} Is element in viewport
         */
        isInViewport(element) {
            const rect = element.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );
        },

        /**
         * Animate element with CSS classes
         * @param {HTMLElement} element - Element to animate
         * @param {string} animationClass - CSS animation class
         * @param {number} duration - Animation duration
         */
        animate(element, animationClass, duration = APP_CONFIG.animation.fadeInDuration) {
            element.classList.add(animationClass);
            setTimeout(() => {
                element.classList.remove(animationClass);
            }, duration);
        },

        /**
         * Format currency value
         * @param {number} value - Numeric value
         * @returns {string} Formatted currency string
         */
        formatCurrency(value) {
            return new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            }).format(value);
        },

        /**
         * Validate email format
         * @param {string} email - Email to validate
         * @returns {boolean} Is valid email
         */
        isValidEmail(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        }
    };

    /**
     * Navigation Component
     */
    class NavigationController {
        constructor() {
            this.navbar = document.querySelector('.navbar');
            this.navLinks = document.querySelectorAll('.nav-link');
            this.mobileToggler = document.querySelector('.navbar-toggler');
            this.navCollapse = document.querySelector('.navbar-collapse');
            
            this.init();
        }

        init() {
            this.bindEvents();
            this.handleScrollEffect();
        }

        bindEvents() {
            // Scroll effect for navbar
            window.addEventListener('scroll', 
                Utils.throttle(() => this.handleScrollEffect(), APP_CONFIG.performance.throttleDelay)
            );

            // Smooth scrolling for anchor links
            this.navLinks.forEach(link => {
                link.addEventListener('click', (e) => this.handleSmoothScroll(e));
            });

            // Close mobile menu on link click
            this.navLinks.forEach(link => {
                link.addEventListener('click', () => this.closeMobileMenu());
            });

            // Close mobile menu on outside click
            document.addEventListener('click', (e) => this.handleOutsideClick(e));
        }

        handleScrollEffect() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > APP_CONFIG.ui.scrollThreshold) {
                this.navbar.classList.add('navbar-scrolled');
            } else {
                this.navbar.classList.remove('navbar-scrolled');
            }
        }

        handleSmoothScroll(event) {
            const href = event.target.getAttribute('href');
            
            if (href && href.startsWith('#')) {
                event.preventDefault();
                const targetElement = document.querySelector(href);
                
                if (targetElement) {
                    const offsetTop = targetElement.offsetTop - APP_CONFIG.ui.navbarOffset;
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            }
        }

        closeMobileMenu() {
            if (window.innerWidth <= APP_CONFIG.ui.mobileBreakpoint) {
                const bsCollapse = new bootstrap.Collapse(this.navCollapse, {
                    hide: true
                });
            }
        }

        handleOutsideClick(event) {
            if (!this.navbar.contains(event.target) && 
                this.navCollapse.classList.contains('show')) {
                this.closeMobileMenu();
            }
        }
    }

    /**
     * Typewriter Animation Component
     */
    class TypewriterEffect {
        constructor(element, options = {}) {
            this.element = element;
            this.text = element.textContent;
            this.options = {
                speed: options.speed || APP_CONFIG.animation.typewriterSpeed,
                delay: options.delay || 0,
                loop: options.loop || false,
                cursor: options.cursor || '|'
            };
            
            this.currentIndex = 0;
            this.isDeleting = false;
            
            this.init();
        }

        init() {
            if (!this.element || !this.text) return;
            
            this.element.textContent = '';
            
            setTimeout(() => {
                this.startAnimation();
            }, this.options.delay);
        }

        startAnimation() {
            const currentText = this.isDeleting 
                ? this.text.substring(0, this.currentIndex - 1)
                : this.text.substring(0, this.currentIndex + 1);

            this.element.textContent = currentText + this.options.cursor;

            if (!this.isDeleting && this.currentIndex === this.text.length) {
                if (this.options.loop) {
                    setTimeout(() => {
                        this.isDeleting = true;
                        this.startAnimation();
                    }, 2000);
                } else {
                    this.element.textContent = this.text;
                }
                return;
            }

            if (this.isDeleting && this.currentIndex === 0) {
                this.isDeleting = false;
                this.startAnimation();
                return;
            }

            this.currentIndex += this.isDeleting ? -1 : 1;
            
            setTimeout(() => {
                this.startAnimation();
            }, this.options.speed);
        }
    }

    /**
     * Form Validation Component
     */
    class FormValidator {
        constructor(formElement) {
            this.form = formElement;
            this.fields = this.form.querySelectorAll('input, textarea, select');
            
            this.init();
        }

        init() {
            this.bindEvents();
        }

        bindEvents() {
            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
            
            this.fields.forEach(field => {
                field.addEventListener('blur', () => this.validateField(field));
                field.addEventListener('input', () => this.clearFieldError(field));
            });
        }

        handleSubmit(event) {
            event.preventDefault();
            
            if (this.validateForm()) {
                this.submitForm();
            }
        }

        validateForm() {
            let isValid = true;
            
            this.fields.forEach(field => {
                if (!this.validateField(field)) {
                    isValid = false;
                }
            });
            
            return isValid;
        }

        validateField(field) {
            const value = field.value.trim();
            const fieldType = field.type;
            const isRequired = field.hasAttribute('required');
            
            this.clearFieldError(field);
            
            if (isRequired && !value) {
                this.showFieldError(field, 'Este campo é obrigatório');
                return false;
            }
            
            if (fieldType === 'email' && value && !Utils.isValidEmail(value)) {
                this.showFieldError(field, 'Formato de email inválido');
                return false;
            }
            
            if (fieldType === 'tel' && value && !this.isValidPhone(value)) {
                this.showFieldError(field, 'Formato de telefone inválido');
                return false;
            }
            
            return true;
        }

        isValidPhone(phone) {
            const phoneRegex = /^(\(?\d{2}\)?\s?)?(\d{4,5})-?(\d{4})$/;
            return phoneRegex.test(phone);
        }

        showFieldError(field, message) {
            field.classList.add('is-invalid');
            
            let errorElement = field.parentNode.querySelector('.invalid-feedback');
            if (!errorElement) {
                errorElement = document.createElement('div');
                errorElement.className = 'invalid-feedback';
                field.parentNode.appendChild(errorElement);
            }
            
            errorElement.textContent = message;
        }

        clearFieldError(field) {
            field.classList.remove('is-invalid');
            
            const errorElement = field.parentNode.querySelector('.invalid-feedback');
            if (errorElement) {
                errorElement.remove();
            }
        }

        async submitForm() {
            const formData = new FormData(this.form);
            const submitButton = this.form.querySelector('[type="submit"]');
            
            this.setSubmitState(submitButton, true);
            
            try {
                const response = await fetch(this.form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                    }
                });
                
                if (response.ok) {
                    this.showSuccessMessage();
                    this.form.reset();
                } else {
                    throw new Error('Erro ao enviar formulário');
                }
            } catch (error) {
                this.showErrorMessage(error.message);
            } finally {
                this.setSubmitState(submitButton, false);
            }
        }

        setSubmitState(button, isLoading) {
            if (isLoading) {
                button.disabled = true;
                button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Enviando...';
            } else {
                button.disabled = false;
                button.innerHTML = button.dataset.originalText || 'Enviar';
            }
        }

        showSuccessMessage() {
            const alert = this.createAlert('success', 'Mensagem enviada com sucesso!');
            this.form.parentNode.insertBefore(alert, this.form);
        }

        showErrorMessage(message) {
            const alert = this.createAlert('danger', message);
            this.form.parentNode.insertBefore(alert, this.form);
        }

        createAlert(type, message) {
            const alert = document.createElement('div');
            alert.className = `alert alert-${type} alert-dismissible fade show`;
            alert.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            setTimeout(() => {
                alert.remove();
            }, 5000);
            
            return alert;
        }
    }

    /**
     * Animation Observer Component
     */
    class AnimationObserver {
        constructor() {
            this.animatedElements = document.querySelectorAll('[data-animate]');
            this.init();
        }

        init() {
            if (!this.animatedElements.length) return;
            
            this.createObserver();
            this.observeElements();
        }

        createObserver() {
            const options = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };
            
            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.animateElement(entry.target);
                        this.observer.unobserve(entry.target);
                    }
                });
            }, options);
        }

        observeElements() {
            this.animatedElements.forEach(element => {
                this.observer.observe(element);
            });
        }

        animateElement(element) {
            const animationType = element.dataset.animate;
            const delay = parseInt(element.dataset.delay) || 0;
            
            setTimeout(() => {
                element.classList.add('animate__animated', `animate__${animationType}`);
            }, delay);
        }
    }

    /**
     * Performance Monitor
     */
    class PerformanceMonitor {
        constructor() {
            this.init();
        }

        init() {
            this.monitorPageLoad();
            this.monitorUserInteractions();
        }

        monitorPageLoad() {
            window.addEventListener('load', () => {
                const loadTime = performance.now();
                console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
                
                if (loadTime > 3000) {
                    console.warn('Page load time is slow. Consider optimization.');
                }
            });
        }

        monitorUserInteractions() {
            ['click', 'scroll', 'resize'].forEach(eventType => {
                window.addEventListener(eventType, 
                    Utils.throttle(() => {
                        console.log(`User interaction: ${eventType}`);
                    }, 1000)
                );
            });
        }
    }

    /**
     * Application Initializer
     */
    class AppInitializer {
        constructor() {
            this.init();
        }

        init() {
            this.initializeComponents();
            this.bindGlobalEvents();
        }

        initializeComponents() {
            // Initialize Navigation
            new NavigationController();

            // Initialize Typewriter Effect
            const typewriterElements = document.querySelectorAll('.typewriter-text');
            typewriterElements.forEach(element => {
                new TypewriterEffect(element, {
                    speed: 100,
                    delay: 500
                });
            });

            // Initialize Form Validation
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                new FormValidator(form);
            });

            // Initialize Animation Observer
            new AnimationObserver();

            // Initialize Performance Monitor (development only)
            if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
                new PerformanceMonitor();
            }
        }

        bindGlobalEvents() {
            // Back to top button
            this.initBackToTop();
            
            // Image lazy loading fallback
            this.initImageLazyLoading();
            
            // External links
            this.initExternalLinks();
        }

        initBackToTop() {
            const backToTopButton = document.getElementById('back-to-top');
            if (!backToTopButton) return;

            window.addEventListener('scroll', 
                Utils.throttle(() => {
                    if (window.pageYOffset > 300) {
                        backToTopButton.style.display = 'block';
                    } else {
                        backToTopButton.style.display = 'none';
                    }
                }, APP_CONFIG.performance.throttleDelay)
            );

            backToTopButton.addEventListener('click', (e) => {
                e.preventDefault();
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        }

        initImageLazyLoading() {
            const images = document.querySelectorAll('img[data-src]');
            
            if ('IntersectionObserver' in window) {
                const imageObserver = new IntersectionObserver((entries) => {
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
            } else {
                // Fallback for older browsers
                images.forEach(img => {
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                });
            }
        }

        initExternalLinks() {
            const externalLinks = document.querySelectorAll('a[href^="http"]:not([href*="' + window.location.hostname + '"])');
            
            externalLinks.forEach(link => {
                link.setAttribute('target', '_blank');
                link.setAttribute('rel', 'noopener noreferrer');
            });
        }
    }

    /**
     * Initialize Application on DOM Ready
     */
    document.addEventListener('DOMContentLoaded', () => {
        new AppInitializer();
    });

    /**
     * Global Error Handler
     */
    window.addEventListener('error', (event) => {
        console.error('Global error:', event.error);
        
        // Send error to monitoring service in production
        if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
            // Implementation for error tracking service
        }
    });

    // Expose utilities globally for external scripts
    window.RegionalVeiculos = {
        Utils,
        TypewriterEffect,
        FormValidator
    };

})();
